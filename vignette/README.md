# Kenya Clinical Vignettes Evaluation Dataset

A maternal, neonatal, child, and sexual/reproductive health subset extracted from a Kenyan primary healthcare benchmarking study, where 145 nurses across three counties wrote clinical case scenarios and expert clinicians provided reference responses.

## Dataset Summary

| File | Vignettes | Description |
|------|-----------|-------------|
| `data/obgyn_vignettes.tsv` | 284 | Clinical vignettes with expert responses |

Category breakdown: **Child Health** (115), **Sexual & Reproductive Health** (71), **Maternal** (59), **Neonatal** (39).

## Data Format

### Vignettes (`obgyn_vignettes.tsv`)

| Column | Description |
|--------|-------------|
| `study_id` | Unique vignette identifier |
| `scenario` | The nurse's clinical scenario description |
| `clinician_response` | Expert clinician's reference response |
| `category` | `MATERNAL`, `NEONATAL`, `CHILD_HEALTH`, or `SRH` |

## Usage

Feed `scenario` to an LLM, then compare its response against `clinician_response` (open-ended evaluation).

## Source

Extracted from the original study dataset (507 vignettes) using `scripts/extract_obgyn_vignettes.py`. Each vignette was classified by Gemini (`gemini-3-flash-preview`) into MATERNAL, NEONATAL, CHILD_HEALTH, SRH, or OTHER.

- Paper: [Benchmarking Large Language Models and Clinicians Using Locally Generated Primary Healthcare Vignettes in Kenya](https://doi.org/10.1101/2025.10.25.25338798) (Mwaniki et al., 2025)

## License

The original dataset is shared under the terms of the associated preprint. See the paper for details.

## Citation

```bibtex
@article{mwaniki2025benchmarking,
  title={Benchmarking Large Language Models and Clinicians Using Locally Generated Primary Healthcare Vignettes in Kenya},
  author={Mwaniki, Paul and others},
  journal={medRxiv},
  year={2025},
  doi={10.1101/2025.10.25.25338798}
}
```

## Directory Structure

```
vignette/
├── README.md
├── LICENSE
├── data/
│   └── obgyn_vignettes.tsv                (284 clinical vignettes)
├── scripts/
│   └── extract_obgyn_vignettes.py         (extraction script)
├── datasets/
│   ├── Combined review data.csv           (expert panel ratings)
│   └── Prompt responses.xlsx              (clinician & LLM responses)
└── 2025.10.25.25338798v1.full.pdf         (original paper)
```
