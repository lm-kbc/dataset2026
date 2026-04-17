# AKBC Shared Task 2026: Knowledge Base Construction from Language Models (5th Edition)

This repository hosts data for the [AKBC Shared Task](https://lm-kbc.github.io/challenge2026/) at [AKBC](https://www.akbc.ws/2026/) / [EMNLP 2026](https://2026.emnlp.org/) in Budapest.

This repository contains:

- The [dataset](data/) for the shared task
- [Evaluation script](evaluate.py)
- [Baseline code](models/)
- Instructions for submitting your predictions

## Table of contents

1. [News](#news)
2. [Challenge overview](#challenge-overview)
3. [Dataset](#dataset)
4. [Evaluation metrics](#evaluation-metrics)
5. [Getting started](#getting-started)
    - [Setup](#setup)
    - [How to structure your prediction file](#how-to-structure-your-prediction-file)
    - [Submit your predictions](#submit-your-predictions)

## News

- **April 2026**: Release of dataset, baseline, and evaluation script

## Challenge overview

Pretrained language models (LMs) contain a substantial amount of factual knowledge. Turning that knowledge into reliable knowledge base entries, however, is much harder than answering a single factual question. In this shared task, we invite participants to build knowledge bases from LMs for given subjects and relations. In crucial difference to existing probing benchmarks like LAMA ([Petroni et al., 2019](https://arxiv.org/pdf/1909.01066.pdf)), we make no simplifying assumptions on relation cardinalities, i.e., a subject-entity can stand in relation with zero, one, or many object-entities.

Unlike earlier editions, this version does **not require entity disambiguation**. Predictions are evaluated as **strings** using normalization and alias matching.

> Formally, given the input subject-entity (s) and relation (r), the task is to
> predict all the correct
> object-entities ({o<sub>1</sub>, o<sub>2</sub>, ..., o<sub>k</sub>}) using LM
> probing.

## Dataset

Number of unique subject-entities in the data splits.

<table>
<thead>
    <tr>
        <th>Relation</th>
        <th>Train</th>
        <th>Val</th>
        <th>Test</th>
        <th>Special features</th>
    </tr>
</thead>
<tbody>
    <tr>
        <td>countryLandBordersCountry</td>
        <td>68</td>
        <td>68</td>
        <td>67</td>
        <td>Null values possible</td>
    </tr>
    <tr>
        <td>personHasCityOfDeath</td>
        <td>100</td>
        <td>100</td>
        <td>100</td>
        <td>Null values possible</td>
    </tr>
    <tr>
        <td>hasCapacity</td>
        <td>100</td>
        <td>100</td>
        <td>100</td>
        <td>Object is numeric</td>
    </tr>
    <tr>
        <td>awardWonBy</td>
        <td>10</td>
        <td>10</td>
        <td>10</td>
        <td>Many objects per subject</td>
    </tr>
    <tr>
        <td>companyTradesAtStockExchange</td>
        <td>100</td>
        <td>100</td>
        <td>100</td>
        <td>Null values possible</td>
    </tr>
        <tr>
        <td>hasArea</td>
        <td>100</td>
        <td>100</td>
        <td>100</td>
        <td>Object is numeric (square km)</td>
    </tr>
</tbody>
</table>

## Evaluation metrics

We evaluate predictions using **macro precision, recall, and F1-score**.

For **string relations**, predicted strings are normalized (lowercased, diacritics removed, punctuation stripped) and matched against the ground-truth label and its known aliases.
For **numeric relations** (`hasCapacity`, `hasArea`), a prediction is correct if it falls within **5% relative tolerance** of the ground-truth value.

See the evaluation script ([evaluate.py](evaluate.py)) for details.

```bash
python evaluate.py \
  -g data/val.jsonl \
  -p your_predictions.jsonl
```

Parameters: ``-g`` (the ground truth file), ``-p`` (the prediction file).

## Getting started

### Setup

1. Clone this repository:

    ```bash
    mkdir lm-kbc-2026
    cd lm-kbc-2026
    git clone https://github.com/lm-kbc/dataset2026.git
    cd dataset2026
    ```

2. Create a virtual environment and install the requirements:

    ```bash
    conda create -n lm-kbc-2026 python=3.11
    ```

    ```bash
    conda activate lm-kbc-2026
    pip install -r requirements.txt
    ```

3. Write your own solution and generate predictions (format described
   in [How to structure your prediction file](#how-to-structure-your-prediction-file)).
4. Evaluate your predictions using the evaluation script
   (see [Evaluation metrics](#evaluation-metrics)).
5. Submit your predictions
   (see [Submit your predictions](#submit-your-predictions)).

### How to structure your prediction file

Your prediction file should be in the jsonl format.
Each line of a valid prediction file contains a JSON object which must
contain at least 3 fields to be used by the evaluation script:

- ``SubjectEntity``: the subject entity (string)
- ``Relation``: the relation (string)
- ``ObjectEntities``: the predicted object entity strings (list of strings)

This is an example of how to write a prediction file:

```python
import json

# Dummy predictions
predictions = [
    {
        "SubjectEntity": "Dominican republic",
        "Relation": "countryLandBordersCountry",
        "ObjectEntities": ["Haiti"]
    },
    {
        "SubjectEntity": "Jiaxing Stadium in Jiaxing",
        "Relation": "hasCapacity",
        "ObjectEntities": ["35000"]
    },
    {
        "SubjectEntity": "Mauritius",
        "Relation": "countryLandBordersCountry",
        "ObjectEntities": []
    }

]

fp = "./path/to/your/prediction/file.jsonl"

with open(fp, "w") as f:
    for pred in predictions:
        f.write(json.dumps(pred) + "\n")
```

### Submit your predictions

Submit your system paper via [OpenReview](https://openreview.net/group?id=EMNLP/2026/Workshop/LM-KBC_Shared_Task).

For the leaderboard, submit your predictions to CodaLab (link TBA).
