# MedQA-USMLE OBGYN Evaluation Dataset

An Obstetrics & Gynecology subset extracted from [MedQA](https://github.com/jind11/MedQA), a large-scale open-domain QA dataset of USMLE-style clinical board questions.

## Dataset Summary

| File | Questions | Description |
|------|-----------|-------------|
| `data/obgyn_usmle.tsv` | 1,025 | OBGYN MCQs with answers |

Category breakdown: **Obstetrics** (497), **Gynecology** (395), **Reproductive Health** (133).

## Data Format

### MCQ (`obgyn_usmle.tsv`)

| Column | Description |
|--------|-------------|
| `question` | The clinical vignette / question text |
| `options_formatted` | Answer choices: `A. ... \| B. ... \| C. ... \| D. ...` |
| `correct_letter` | Correct answer letter (A–F) |
| `answer` | Correct answer text |
| `category` | `OBSTETRICS`, `GYNECOLOGY`, or `REPRODUCTIVE_HEALTH` |
| `meta_info` | USMLE step: `step1` or `step2` |

## Usage

Feed `question` + `options_formatted` to an LLM, compare its letter choice against `correct_letter`.

## Source

Extracted from the MedQA US question bank (14,369 questions) using `extract_obgyn_usmle.py`. Each question was classified by Gemini (`gemini-3-flash-preview`) into OBSTETRICS, GYNECOLOGY, REPRODUCTIVE_HEALTH, or NONE.

- Paper: [What Disease does this Patient Have? A Large-scale Open Domain Question Answering Dataset from Medical Exams](https://arxiv.org/abs/2009.13081) (Jin et al., 2020)
- Repository: [jind11/MedQA](https://github.com/jind11/MedQA)

## License

MIT (inherited from MedQA).

## Citation

```bibtex
@article{jin2020disease,
  title={What Disease does this Patient Have? A Large-scale Open Domain Question Answering Dataset from Medical Exams},
  author={Jin, Di and Pan, Eileen and Oufattole, Nassim and Weng, Wei-Hung and Fang, Hanyi and Szolovits, Peter},
  journal={arXiv preprint arXiv:2009.13081},
  year={2020}
}
```

## Directory Structure

```
medqa-usmle/
├── README.md
├── LICENSE
├── 2009.13081v1.pdf                (original paper)
├── extract_obgyn_usmle.py         (extraction script)
├── data/
│   └── obgyn_usmle.tsv            (1,025 OBGYN MCQs)
└── source/
    └── US_qbank.jsonl              (14,369 source questions)
```
