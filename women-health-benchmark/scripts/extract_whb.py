"""
Extract Women's Health Benchmark model stumps from WHB subset

Reads the WHB subset JSON (Gruber et al., 2025) and outputs a clean TSV
with expert prompts and justifications.

Source: https://huggingface.co/datasets/TheLumos/WHB_subset

Usage:
    python extract_whb.py

Requires:
    pip install pandas
"""

import json
from pathlib import Path

import pandas as pd

SCRIPT_DIR = Path(__file__).parent
DATA_DIR = SCRIPT_DIR.parent / "data"
SOURCE_DIR = SCRIPT_DIR.parent / "sources"

SOURCE_JSON = SOURCE_DIR / "WHB_subset.json"


def clean_text(text):
    """Escape newlines as literal \\n and strip whitespace."""
    if pd.isna(text):
        return text
    return str(text).replace("\r\n", "\\n").replace("\r", "\\n").replace("\n", "\\n").strip()


def main():
    # ── Load data ─────────────────────────────────────────────
    print("Loading WHB subset...")
    with open(SOURCE_JSON, "r", encoding="utf-8") as f:
        records = json.load(f)

    df = pd.DataFrame(records)
    print(f"  Total: {len(df)} model stumps")

    # ── Clean text ────────────────────────────────────────────
    df["question_clean"] = df["expert_prompt"].apply(clean_text)
    df["expert_justification"] = df["justification"].apply(clean_text)

    # ── Output TSV ────────────────────────────────────────────
    DATA_DIR.mkdir(exist_ok=True)

    out = df[["question_clean", "expert_justification"]]
    out.to_csv(DATA_DIR / "womens_health_stumps.tsv", sep="\t", index=False)
    print(f"\n  Saved {len(out)} model stumps → data/womens_health_stumps.tsv")

    # ── Summary ───────────────────────────────────────────────
    print("\n" + "=" * 60)
    print("EXTRACTION COMPLETE")
    print("=" * 60)
    print(f"Source: {len(records)} WHB model stumps")
    print(f"Extracted: {len(out)} model stumps with expert justifications")


if __name__ == "__main__":
    main()
