"""
Extract OBGYN MCQs and SAQs from AfriMed-QA v2

Filters the AfriMed-QA dataset (Olatunji et al., 2024) to expert-tier
Obstetrics & Gynecology questions, then formats MCQs and SAQs as TSVs.

Source: https://huggingface.co/datasets/intronhealth/afrimedqa_v2

Usage:
    python extract_obgyn.py

Requires:
    pip install pandas
"""

import json
from pathlib import Path

import pandas as pd

SCRIPT_DIR = Path(__file__).parent
DATA_DIR = SCRIPT_DIR.parent / "data"
SOURCE_DIR = SCRIPT_DIR.parent / "sources"

SOURCE_CSV = SOURCE_DIR / "afri_med_qa_15k_v2.4_phase_2_15275.csv"


def clean_text(text):
    """Escape newlines as literal \\n and strip whitespace."""
    if pd.isna(text):
        return text
    return str(text).replace("\r\n", "\\n").replace("\r", "\\n").replace("\n", "\\n").strip()


def parse_options(row):
    """Parse JSON options and correct_answer into formatted strings."""
    opts = json.loads(row["answer_options"])
    letters = {f"option{i}": chr(64 + i) for i in range(1, 6)}  # option1→A, ...

    formatted = " | ".join(f"{letters[k]}. {v}" for k, v in opts.items())
    answer_letters = ",".join(
        letters[o.strip()] for o in row["correct_answer"].split(",")
    )
    return formatted, answer_letters


def main():
    # ── Load data ─────────────────────────────────────────────
    print("Loading AfriMed-QA...")
    df = pd.read_csv(SOURCE_CSV)
    print(f"  Total: {len(df)} rows")

    # ── Filter to expert-tier OBGYN MCQs + SAQs ──────────────
    obgyn = df[
        (df["specialty"].str.contains("Obstetric", case=False, na=False))
        & (df["question_type"].isin(["mcq", "saq"]))
        & (df["tier"] == "expert")
    ].copy()
    print(f"  OBGYN expert MCQ+SAQ: {len(obgyn)}")

    # ── Clean text ────────────────────────────────────────────
    obgyn["question_clean"] = obgyn["question_clean"].apply(clean_text)
    obgyn["answer_rationale"] = obgyn["answer_rationale"].apply(clean_text)

    DATA_DIR.mkdir(exist_ok=True)

    # ── Extract MCQs ──────────────────────────────────────────
    mcq = obgyn[obgyn["question_type"] == "mcq"].copy()
    mcq[["options_formatted", "correct_letter"]] = mcq.apply(
        parse_options, axis=1, result_type="expand"
    )
    mcq_out = mcq[["question_clean", "options_formatted", "correct_letter"]]
    mcq_out.to_csv(DATA_DIR / "obgyn_mcq.tsv", sep="\t", index=False)
    print(f"\n  Saved {len(mcq_out)} MCQs → data/obgyn_mcq.tsv")

    # ── Extract SAQs ──────────────────────────────────────────
    saq_out = obgyn[obgyn["question_type"] == "saq"][
        ["question_clean", "answer_rationale"]
    ].copy()
    saq_out.to_csv(DATA_DIR / "obgyn_saq.tsv", sep="\t", index=False)
    print(f"  Saved {len(saq_out)} SAQs → data/obgyn_saq.tsv")

    # ── Summary ───────────────────────────────────────────────
    print("\n" + "=" * 60)
    print("EXTRACTION COMPLETE")
    print("=" * 60)
    print(f"Source: {len(df)} AfriMed-QA questions")
    print(f"Extracted: {len(mcq_out)} MCQs + {len(saq_out)} SAQs")

    multi = mcq_out["correct_letter"].str.contains(",").sum()
    print(f"\nMCQs with multiple correct answers: {multi} / {len(mcq_out)}")


if __name__ == "__main__":
    main()
