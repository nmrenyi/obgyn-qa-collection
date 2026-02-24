"""
Extract OBGYN & Pediatrics MCQs from MedMCQA

Filters the MedMCQA dataset (Pal et al., 2022) to Gynaecology & Obstetrics
and Pediatrics subjects, then formats the output to match the afrimedqa
data layout.

Source: https://huggingface.co/datasets/openlifescienceai/medmcqa

Usage:
    python extract_obgyn.py

Requires:
    pip install pandas pyarrow
"""

from pathlib import Path

import pandas as pd

SCRIPT_DIR = Path(__file__).parent
DATA_DIR = SCRIPT_DIR.parent / "data"
SOURCE_DIR = SCRIPT_DIR.parent / "sources"

SUBJECTS = ["Gynaecology & Obstetrics", "Pediatrics"]
COP_MAP = {0: "A", 1: "B", 2: "C", 3: "D"}


def load_split(name):
    """Load a parquet split from sources/."""
    path = SOURCE_DIR / f"{name}-00000-of-00001.parquet"
    df = pd.read_parquet(path)
    df["split"] = name
    return df


def format_options(row):
    """Format options as 'A. ... | B. ... | C. ... | D. ...'."""
    parts = []
    for letter, col in zip("ABCD", ["opa", "opb", "opc", "opd"]):
        text = str(row[col]).strip()
        parts.append(f"{letter}. {text}")
    return " | ".join(parts)


def main():
    # ── Load train + validation (test has no answers) ────────
    print("Loading MedMCQA splits...")
    splits = []
    for name in ["train", "validation"]:
        df = load_split(name)
        print(f"  {name}: {len(df)} rows")
        splits.append(df)

    full = pd.concat(splits, ignore_index=True)
    print(f"  Total: {len(full)} rows")
    print("  (test split skipped — answers withheld by original authors)")

    # ── Filter to OBGYN + Pediatrics ──────────────────────────
    obgyn = full[full["subject_name"].isin(SUBJECTS)].copy()
    print(f"\nFiltered to {SUBJECTS}:")
    for subj, count in obgyn["subject_name"].value_counts().items():
        print(f"  {subj}: {count}")
    print(f"  Total: {len(obgyn)}")

    # ── Format MCQs ───────────────────────────────────────────
    DATA_DIR.mkdir(exist_ok=True)

    obgyn["options_formatted"] = obgyn.apply(format_options, axis=1)
    obgyn["correct_letter"] = obgyn["cop"].map(COP_MAP)

    mcq_out = obgyn[
        ["id", "question", "options_formatted", "correct_letter",
         "exp", "subject_name", "topic_name", "choice_type", "split"]
    ].copy()
    mcq_out.columns = [
        "id", "question", "options_formatted", "correct_letter",
        "explanation", "subject", "topic", "choice_type", "split"
    ]
    mcq_out = mcq_out.sort_values(["subject", "id"]).reset_index(drop=True)

    # Clean newlines so each row stays on one line in the TSV
    for col in ["question", "explanation"]:
        mcq_out[col] = mcq_out[col].apply(
            lambda x: str(x).replace("\r\n", "\\n").replace("\r", "\\n").replace("\n", "\\n").strip()
            if pd.notna(x) else x
        )

    mcq_path = DATA_DIR / "obgyn_mcq.tsv"
    mcq_out.to_csv(mcq_path, sep="\t", index=False)
    print(f"\nSaved {len(mcq_out)} MCQs → {mcq_path.relative_to(SCRIPT_DIR.parent)}")

    # ── Summary ───────────────────────────────────────────────
    print("\n" + "=" * 60)
    print("EXTRACTION COMPLETE")
    print("=" * 60)
    print(f"Source: {len(full)} MedMCQA questions (train + validation)")
    print(f"Extracted: {len(mcq_out)} OBGYN + Pediatrics MCQs")

    # ── Subject/topic breakdown ───────────────────────────────
    print("\nSubject breakdown:")
    for subj, count in mcq_out["subject"].value_counts().items():
        print(f"  {subj}: {count}")

    print(f"\nExplanations available: {mcq_out['explanation'].notna().sum()} / {len(mcq_out)}")
    print(f"Choice type: {mcq_out['choice_type'].value_counts().to_dict()}")


if __name__ == "__main__":
    main()
