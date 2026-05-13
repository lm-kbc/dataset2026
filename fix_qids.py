#!/usr/bin/env python3
"""
Replace Q-IDs in SubjectEntity fields with labels from Spanish Wikipedia.

Entities like "Q5847811 in Lima" appear when Wikidata has no English label
for an entity but links to a Spanish Wikipedia article. This script fetches
the Spanish Wikipedia article title via the Wikidata API and uses it as the
label.
"""

import json
import re
import sys
import time

import requests

WIKIDATA_API = "https://www.wikidata.org/w/api.php"
QID_PATTERN = re.compile(r"^(Q\d+)(\s.*)$")


def get_labels_from_wikidata(qids: list[str]) -> dict[str, str]:
    """Return a mapping from QID to best available label.

    Priority order:
    1. English label
    2. Spanish label
    3. Spanish Wikipedia article title (eswiki sitelink)
    4. Portuguese label (common for Brazilian venues)
    """
    params = {
        "action": "wbgetentities",
        "ids": "|".join(qids),
        "props": "labels|sitelinks",
        "sitefilter": "eswiki",
        "languages": "en|es|pt",
        "format": "json",
    }
    response = requests.get(WIKIDATA_API, params=params, timeout=30)
    response.raise_for_status()
    data = response.json()

    labels: dict[str, str] = {}
    for qid in qids:
        entity = data.get("entities", {}).get(qid, {})
        entity_labels = entity.get("labels", {})
        sitelinks = entity.get("sitelinks", {})

        label = (
            entity_labels.get("en", {}).get("value")
            or entity_labels.get("es", {}).get("value")
            or sitelinks.get("eswiki", {}).get("title")
            or entity_labels.get("pt", {}).get("value")
        )
        if label:
            labels[qid] = label
        else:
            print(f"WARNING: No label found for {qid}", file=sys.stderr)

    return labels


def fix_file(path: str, qid_to_label: dict[str, str]) -> int:
    """Fix Q-IDs in SubjectEntity fields in a JSONL file. Returns number of replacements."""
    lines = []
    replacements = 0
    with open(path) as f:
        for line in f:
            obj = json.loads(line)
            subject = obj.get("SubjectEntity", "")
            m = QID_PATTERN.match(subject)
            if m:
                qid, suffix = m.group(1), m.group(2)
                label = qid_to_label.get(qid)
                if label:
                    new_subject = label + suffix
                    print(f"  {subject!r} -> {new_subject!r}")
                    obj["SubjectEntity"] = new_subject
                    replacements += 1
                else:
                    print(f"  WARNING: Could not resolve {qid!r}, leaving as-is", file=sys.stderr)
            lines.append(json.dumps(obj, ensure_ascii=False))

    with open(path, "w") as f:
        f.write("\n".join(lines) + "\n")

    return replacements


def collect_qids(paths: list[str]) -> list[str]:
    """Collect all unique Q-IDs from SubjectEntity fields across files."""
    qids: set[str] = set()
    for path in paths:
        with open(path) as f:
            for line in f:
                obj = json.loads(line)
                subject = obj.get("SubjectEntity", "")
                m = QID_PATTERN.match(subject)
                if m:
                    qids.add(m.group(1))
    return sorted(qids)


def main():
    data_files = ["data/train.jsonl", "data/val.jsonl", "data/test.jsonl"]

    print("Collecting Q-IDs from data files...")
    qids = collect_qids(data_files)
    if not qids:
        print("No Q-IDs found in SubjectEntity fields.")
        return

    print(f"Found {len(qids)} unique Q-IDs: {qids}")

    # Fetch labels in batches of 50 (Wikidata API limit)
    qid_to_label: dict[str, str] = {}
    batch_size = 50
    for i in range(0, len(qids), batch_size):
        batch = qids[i : i + batch_size]
        print(f"\nFetching labels for batch: {batch}")
        labels = get_labels_from_wikidata(batch)
        qid_to_label.update(labels)
        if i + batch_size < len(qids):
            time.sleep(1)  # Be polite to the API

    print(f"\nResolved labels: {qid_to_label}")

    total = 0
    for path in data_files:
        print(f"\nFixing {path}...")
        count = fix_file(path, qid_to_label)
        print(f"  {count} replacement(s) made.")
        total += count

    print(f"\nDone. Total replacements: {total}")


if __name__ == "__main__":
    main()
