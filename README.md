# LM-KBC: Knowledge Base Construction from Pre-trained Language Models (4th Edition)

Dataset for the 2026 LM-KBC challenge.

## Dataset

Each line in the dataset files (`data/train.jsonl`, `data/val.jsonl`, `data/test.jsonl`) is a JSON object with the following fields:

- `SubjectEntity`: the subject entity (string label)
- `Relation`: the relation (string)
- `ObjectEntities`: the list of correct object entity labels (list of strings; empty list for the test set)

Example:

```json
{"SubjectEntity": "Nobel Prize in Physics", "Relation": "awardWonBy", "ObjectEntities": ["Marie Curie", "Albert Einstein", "Niels Bohr"]}
```

## Evaluation

Predictions are evaluated using macro/micro precision, recall, and F1-score based on **exact label match**.

```bash
python evaluate.py \
  -g data/val.jsonl \
  -p your_predictions.jsonl
```

Parameters: `-g` (ground truth file), `-p` (predictions file).

### Prediction file format

Your prediction file must be in JSONL format. Each line must contain:

- `SubjectEntity`: the subject entity (string)
- `Relation`: the relation (string)
- `ObjectEntities`: the predicted object entity labels (list of strings)

Example:

```python
import json

predictions = [
    {
        "SubjectEntity": "Dominican Republic",
        "Relation": "countryLandBordersCountry",
        "ObjectEntities": ["Haiti"]
    },
    {
        "SubjectEntity": "Eritrea",
        "Relation": "countryLandBordersCountry",
        "ObjectEntities": ["Ethiopia", "Sudan", "Djibouti"]
    },
    {
        "SubjectEntity": "Iceland",
        "Relation": "countryLandBordersCountry",
        "ObjectEntities": []
    }
]

with open("predictions.jsonl", "w") as f:
    for pred in predictions:
        f.write(json.dumps(pred) + "\n")
```
