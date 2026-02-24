# OBGYN-QA: A Collection of Obstetrics & Gynecology QA Datasets for LLM Evaluation

A curated collection of question-answer datasets in Obstetrics & Gynecology (OBGYN), extracted from publicly available medical QA benchmarks. Designed for evaluating large language models on OBGYN clinical knowledge.

## Datasets

| Dataset | MCQs | SAQs | Region | Source |
|---------|------|------|--------|--------|
| [AfriMed-QA](afrimedqa/) | 660 | 37 | Pan-African | [Olatunji et al., 2024](https://arxiv.org/abs/2411.15640) |

## Structure

Each dataset lives in its own directory with a consistent layout:

```
<dataset_name>/
├── README.md          # Dataset-specific description, license, citation
├── data/              # Clean, ready-to-use evaluation files
├── scripts/           # Code to reproduce the extraction
└── sources/           # Original data and paper
```

## Adding a New Dataset

1. Create a new directory: `<dataset_name>/`
2. Follow the structure above
3. Include extraction scripts for reproducibility
4. Document the license and provide proper attribution

## License

Each dataset retains the license of its original source. See individual dataset READMEs for details.
