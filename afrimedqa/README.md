# AfriMed-QA OBGYN Evaluation Dataset

An Obstetrics & Gynecology subset extracted from [AfriMed-QA v2](https://huggingface.co/datasets/intronhealth/afrimedqa_v2), a pan-African multi-specialty medical question-answering benchmark.

## Dataset Summary

| File | Questions | Type | Description |
|------|-----------|------|-------------|
| `data/obgyn_mcq.tsv` | 660 | Expert MCQ | Multiple-choice with lettered options (A-E), single or multiple correct answers |
| `data/obgyn_saq.tsv` | 37 | Expert SAQ | Short-answer questions with reference rationale |

All questions are expert-tier, sourced from medical school professors across 5 African countries (Ghana, Nigeria, Kenya, Malawi, South Africa).

## Data Format

### MCQ (`obgyn_mcq.tsv`)

| Column | Description |
|--------|-------------|
| `question_clean` | The question text |
| `options_formatted` | Answer choices separated by ` \| ` (e.g., `A. Option1 \| B. Option2 \| ...`) |
| `correct_letter` | Correct answer letter(s), comma-separated if multiple (e.g., `C` or `A,C,D`) |

### SAQ (`obgyn_saq.tsv`)

| Column | Description |
|--------|-------------|
| `question_clean` | The question text |
| `answer_rationale` | Reference answer/explanation |

## Usage

Feed `question_clean` + `options_formatted` to an LLM, compare its letter choice against `correct_letter`.

For MCQs with multiple correct answers (112 of 660), evaluation requires checking if the LLM selected all correct options.

## Source

Extracted from the AfriMed-QA v2 dataset using `scripts/extract_obgyn.ipynb`. The original dataset and paper are in `sources/`.

- Paper: [AfriMed-QA: A Pan-African, Multi-Specialty, Medical Question-Answering Benchmark Dataset](https://arxiv.org/abs/2411.15640) (Olatunji et al., 2024)
- Dataset: [intronhealth/afrimedqa_v2](https://huggingface.co/datasets/intronhealth/afrimedqa_v2)
- Project: [afrimedqa.com](https://www.afrimedqa.com)

## License

This dataset is a derivative of AfriMed-QA v2, released under [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/).

## Citation

```bibtex
@article{olatunji2024afrimed,
  title={AfriMed-QA: A Pan-African, Multi-Specialty, Medical Question-Answering Benchmark Dataset},
  author={Olatunji, Tobi and Nimo, Charles and Owodunni, Abraham and Abdullahi, Tassallah and Ayodele, Emmanuel and Sanni, Mardhiyah and Aka, Chinemelu and Omofoye, Folafunmi and Yuehgoh, Foutse and Faniran, Timothy and others},
  journal={arXiv preprint arXiv:2411.15640},
  year={2024}
}
```

## Directory Structure

```
afrimedqa/
├── README.md
├── data/
│   ├── obgyn_mcq.tsv          (660 expert MCQs)
│   └── obgyn_saq.tsv          (37 expert SAQs)
├── scripts/
│   └── extract_obgyn.ipynb    (extraction & formatting code)
└── sources/
    ├── 2411.15640v4.pdf                              (paper)
    ├── afrimedqa_original_readme.md                  (original dataset card)
    └── afri_med_qa_15k_v2.4_phase_2_15275.csv        (full dataset)
```
