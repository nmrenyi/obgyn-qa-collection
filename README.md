# OBGYN-QA: A Collection of Obstetrics & Gynecology QA Datasets for LLM Evaluation

A curated collection of question-answer datasets in Obstetrics & Gynecology (OBGYN), extracted from publicly available medical QA benchmarks. Designed for evaluating large language models on OBGYN clinical knowledge.

## Datasets

| Dataset | Items | Type | Region | Source |
|---------|-------|------|--------|--------|
| [AfriMed-QA](afrimedqa/) | 660 MCQ + 37 SAQ | Expert exam questions | Pan-African (5 countries) | [Olatunji et al., 2024](https://arxiv.org/abs/2411.15640) |
| [MedMCQA](medmcqa/) | 18,508 MCQ | Entrance exam questions | India | [Pal et al., 2022](https://proceedings.mlr.press/v174/pal22a) |
| [Kenya Vignettes](vignette/) | 284 vignettes | Nurse-written clinical cases | Kenya | [Mwaniki et al., 2025](https://doi.org/10.1101/2025.10.25.25338798) |
| [MedQA-USMLE](medqa-usmle/) | 1,025 MCQ | USMLE-style board questions | USA | [Jin et al., 2020](https://arxiv.org/abs/2009.13081) |
| [Women's Health Benchmark](women-health-benchmark/) | 20 stumps | Expert prompts exposing LLM errors | Multi-national | [Gruber et al., 2025](https://arxiv.org/abs/2512.17028) |

### AfriMed-QA

OBGYN subset of a pan-African medical QA benchmark. 660 multiple-choice and 37 short-answer questions authored by medical professors across Ghana, Nigeria, Kenya, Malawi, and South Africa. Questions span expert-level clinical scenarios with single or multiple correct answers.

### MedMCQA

Obstetrics & Gynecology (10,237) and Pediatrics (8,271) questions extracted from the MedMCQA dataset, sourced from Indian AIIMS and NEET PG entrance exams. Each question has 4 options, a correct answer, and an expert explanation (available for 96% of questions). Fine-grained topic labels are included.

### Kenya Vignettes

284 clinical case scenarios related to maternal, neonatal, child, and sexual/reproductive health, written by 145 Kenyan nurses across three counties. Each vignette includes the nurse's clinical scenario and an expert clinician response. Classified into MATERNAL, NEONATAL, CHILD_HEALTH, and SRH categories using `gemini-3-flash-preview`.

### MedQA-USMLE

OBGYN subset extracted from the MedQA dataset of USMLE-style clinical board questions. 1,025 questions classified into Obstetrics (497), Gynecology (395), and Reproductive Health (133) using `gemini-3-flash-preview`. Each question includes answer options, the correct answer, and USMLE step metadata (Step 1 or 2).

### Women's Health Benchmark

20 expert-crafted "model stumps" from the WHB (Gruber et al., 2025) — clinical prompts specifically designed to expose errors in LLM responses on women's health topics. Covers obstetrics & gynecology, emergency medicine, primary care, oncology, and neurology. Each stump includes an expert justification describing what LLMs typically get wrong.

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
