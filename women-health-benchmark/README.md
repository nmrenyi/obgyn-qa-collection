# Women's Health Benchmark (WHB) Evaluation Subset

A subset of the Women's Health Benchmark (Gruber et al., 2025), containing expert-crafted "model stumps" — clinical prompts that expose errors in LLM responses on women's health topics, each paired with an expert justification.

## Dataset Summary

| File | Entries | Type | Description |
|------|---------|------|-------------|
| `data/womens_health_stumps.tsv` | 20 | Model stumps | Expert prompts with justifications describing LLM errors |

Model stumps span five medical specialties (obstetrics & gynecology, emergency medicine, primary care, oncology, neurology) and three query types (patient, clinician, evidence/policy).

## Data Format

### Model Stumps (`womens_health_stumps.tsv`)

| Column | Description |
|--------|-------------|
| `question_clean` | The expert prompt — a realistic clinical scenario or patient question |
| `expert_justification` | Expert explanation of what LLMs typically get wrong, with references |

## Usage

Feed `question_clean` to an LLM, then compare its response against `expert_justification` to check whether the model reproduces the identified error (e.g., missing a critical diagnosis, giving outdated treatment advice, wrong dosage).

## Source

Extracted from the WHB subset using `scripts/extract_whb.py`. The original dataset and paper are in `sources/`.

- Paper: [A Women's Health Benchmark for Large Language Models](https://arxiv.org/abs/2512.17028) (Gruber et al., 2025)
- Dataset: [TheLumos/WHB_subset](https://huggingface.co/datasets/TheLumos/WHB_subset)
- Organization: [The Lumos AI Labs](https://thelumos.ai)

## License

This dataset is released under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).

## Citation

```bibtex
@article{gruber2025womens,
  title={A Women's Health Benchmark for Large Language Models},
  author={Gruber, Victoria-Elisabeth and Marinescu, Razvan and Fajardo, Diego and Nassar, Amin H. and Arkfeld, Christopher and Ludlow, Alexandria and Patel, Shama and Samaei, Mehrnoosh and Klug, Valerie and Huber, Anna and G{\"u}hner, Marcel and Botta i Orfila, Albert and Lagoja, Irene and Tarr, Kimya and Larson, Haleigh and Howard, Mary Beth},
  journal={arXiv preprint arXiv:2512.17028},
  year={2025}
}
```

## Directory Structure

```
women-health-benchmark/
├── README.md
├── data/
│   └── womens_health_stumps.tsv         (20 model stumps)
├── scripts/
│   └── extract_whb.py                   (extraction & formatting code)
└── sources/
    ├── 2512.17028v1.pdf                 (paper)
    ├── WHB_subset.json                  (original JSON from HuggingFace)
    └── whb_original_readme.md           (original dataset card)
```
