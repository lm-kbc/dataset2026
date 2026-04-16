# LM-KBC: Knowledge Base Construction from Pre-trained Language Models (5th Edition)

This repository hosts data for the LM-KBC challenge at ISWC
2026 (https://lm-kbc.github.io/challenge2026/).

This repository contains:

- The dataset for the challenge
- Evaluation script
- Instructions for submitting your predictions

## Table of contents

1. [News](#news)
2. [Challenge overview](#challenge-overview)
3. [Dataset](#dataset)
4. [Evaluation metrics](#evaluation-metrics)
5. [Getting started](#getting-started)
    - [Setup](#setup)
    - [How to structure your prediction file](#how-to-structure-your-prediction-file)
    - [Submit your predictions to CodaLab](#submit-your-predictions-to-codalab)

## News

- Release of dataset

## Challenge overview

Pretrained language models (LMs) like ChatGPT have advanced a range of semantic
tasks and have also shown promise for
knowledge extraction from the models itself. Although several works have
explored this ability in a setting called
probing or prompting, the viability of knowledge base construction from LMs
remains under-explored. In this edition
of this challenge, we invite participants to build actual disambiguated
knowledge bases from LMs, for given subjects and
relations. In crucial difference to existing probing benchmarks like
LAMA ([Petroni et al., 2019](https://arxiv.org/pdf/1909.01066.pdf)), we make no
simplifying assumptions on relation
cardinalities, i.e., a subject-entity can stand in relation with zero, one, or
many object-entities.

Unlike earlier editions, this version does **not require entity disambiguation**. Instead, we
evaluate the predicted object strings directly using string match metrics.

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

We evaluate the predictions using macro precision, recall, and F1-score.
See the evaluation script ([evaluate.py](evaluate.py)) for more details.

```bash
python evaluate.py \
  -g data/val.jsonl \
  -p data/testrun-XYZ.jsonl
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
5. Submit your solutions to the organizers
   (see [Call for Participants](https://lm-kbc.github.io/challenge2026/#call-for-participants)),
   and/or submit your predictions to CodaLab
   (see [Submit your predictions to CodaLab](#submit-your-predictions-to-codalab)).

### How to structure your prediction file

Your prediction file should be in the jsonl format.
Each line of a valid prediction file contains a JSON object which must
contain at least 3 fields to be used by the evaluation script:

- ``SubjectEntity``: the subject entity (string)
- ``Relation``: the relation (string)
- ``ObjectEntities``: the predicted object entity strings
- ``ObjectEntitiesID``: the predicted object entity IDs, which should be a list
  of Wikidata IDs (strings).

This is an example of how to write a prediction file:

```python
import json

# Dummy predictions
predictions = [
    {
        "SubjectEntity": "Dominican republic",
        "Relation": "CountryBordersWithCountry",
        "ObjectEntities": ["Haiti", "Venezuela", "United States", "Germany"],
        "ObjectEntitiesID": ["Q790", "Q717", "Q30", "Q183"]
    },
    {
        "SubjectEntity": "Jiaxing Stadium in Jiaxing",
        "Relation": "hasCapacity",
        "ObjectEntities": ["35000"],
        "ObjectEntitiesID": ["35000"]
    },
    {
        "SubjectEntity": "Mauritius",
        "Relation": "CountryBordersWithCountry",
        "ObjectEntities": [],
        "ObjectEntitiesID": []
    }

]

fp = "./path/to/your/prediction/file.jsonl"

with open(fp, "w") as f:
    for pred in predictions:
        f.write(json.dumps(pred) + "\n")
```

### Submit your predictions to CodaLab

To participate in the competition and join the leaderboard, sign up for your team account at [CodaLab](https://codalab.lisn.upsaclay.fr).
Then register for the competition and submit your predictions at Participate -> Submit / View Results.
