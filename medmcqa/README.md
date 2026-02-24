# MedMCQA OBGYN & Pediatrics Evaluation Dataset

An Obstetrics & Gynecology and Pediatrics subset extracted from [MedMCQA](https://huggingface.co/datasets/openlifescienceai/medmcqa), a large-scale medical MCQ dataset sourced from Indian AIIMS & NEET PG entrance exams.

## Dataset Summary

| File | Questions | Description |
|------|-----------|-------------|
| `data/obgyn_mcq.tsv` | 18,508 | MCQs with answers (train + validation splits) |

Covers two subjects: **Gynaecology & Obstetrics** (10,237) and **Pediatrics** (8,271). The test split (722 questions) is excluded because answers are withheld by the original authors.

## Data Format

### MCQ (`obgyn_mcq.tsv`)

| Column | Description |
|--------|-------------|
| `id` | Unique question identifier (UUID) |
| `question` | The question text |
| `options_formatted` | Answer choices: `A. ... \| B. ... \| C. ... \| D. ...` |
| `correct_letter` | Correct answer letter (A/B/C/D) |
| `explanation` | Expert explanation of the answer (available for 96% of questions) |
| `subject` | `Gynaecology & Obstetrics` or `Pediatrics` |
| `topic` | Fine-grained medical topic |
| `choice_type` | `single` or `multi` (single-option vs multi-suboption choices) |
| `split` | Original split: `train` or `validation` |

## Usage

Feed `question` + `options_formatted` to an LLM, compare its letter choice against `correct_letter`.

## Source

Extracted from the MedMCQA dataset using `scripts/extract_obgyn.py`. The original dataset and dataset card are in `sources/`.

- Paper: [MedMCQA: A Large-scale Multi-Subject Multi-Choice Dataset for Medical domain Question Answering](https://proceedings.mlr.press/v174/pal22a) (Pal et al., 2022)
- Dataset: [openlifescienceai/medmcqa](https://huggingface.co/datasets/openlifescienceai/medmcqa)

## License

Apache 2.0 (inherited from MedMCQA).

## Citation

```bibtex
@InProceedings{pmlr-v174-pal22a,
  title={MedMCQA: A Large-scale Multi-Subject Multi-Choice Dataset for Medical domain Question Answering},
  author={Pal, Ankit and Umapathi, Logesh Kumar and Sankarasubbu, Malaikannan},
  booktitle={Proceedings of the Conference on Health, Inference, and Learning},
  pages={248--260},
  year={2022},
  volume={174},
  series={Proceedings of Machine Learning Research},
  publisher={PMLR}
}
```

## Directory Structure

```
medmcqa/
├── README.md
├── data/
│   └── obgyn_mcq.tsv           (18,508 MCQs with answers)
├── scripts/
│   └── extract_obgyn.py        (extraction script)
└── sources/
    ├── medmcqa_original_readme.md               (original dataset card)
    ├── train-00000-of-00001.parquet             (182,822 train questions)
    ├── validation-00000-of-00001.parquet        (4,183 validation questions)
    └── test-00000-of-00001.parquet              (6,150 test questions)
```
