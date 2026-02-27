"""
Extract OBGYN / MCH / SRH Vignettes from Kenya Benchmark Dataset

Classifies all 507 clinical vignettes using Gemini, then extracts those related to
obstetrics & gynecology, maternal health, child health, neonatal care, and sexual
& reproductive health.

Source: Mwaniki et al., 2025 — Kenya LLM benchmarking study

Usage:
    python extract_obgyn_vignettes.py

Requires:
    - GEMINI_API_KEY environment variable (or paste it below)
    - pip install google-generativeai pandas openpyxl
"""

import os
import re
import time
from pathlib import Path

import google.generativeai as genai
import pandas as pd

# ============================================================
# CONFIGURATION
# ============================================================
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")  # or paste your key here
GEMINI_MODEL = "gemini-3-flash-preview"
BATCH_SIZE = 10
RATE_LIMIT_SECONDS = 1

SCRIPT_DIR = Path(__file__).parent
DATA_DIR = SCRIPT_DIR.parent / "data"
DATASETS_DIR = SCRIPT_DIR.parent / "datasets"

RESPONSES_FILE = DATASETS_DIR / "Prompt responses.xlsx"

# ============================================================
# CLASSIFICATION PROMPT
# ============================================================
BATCH_CLASSIFICATION_PROMPT = """You are a clinical classifier. Given a BATCH of clinical scenarios from a Kenyan primary care setting, determine whether EACH is related to ANY of the following categories:

1. MATERNAL — pregnancy, childbirth, antenatal/postnatal care, obstetric complications, maternal health
2. NEONATAL — care of newborns (0-28 days), neonatal sepsis, jaundice, prematurity
3. CHILD_HEALTH — health of children/infants/adolescents (under 18), pediatric conditions, immunization, growth/nutrition
4. SRH — sexual and reproductive health: family planning, contraception, STIs, gynecology, GBV/defilement, menstrual disorders

For EACH scenario, respond with EXACTLY one line in this format:
STUDY_ID|YES|CATEGORY  or  STUDY_ID|NO|NONE

Where CATEGORY is one of: MATERNAL, NEONATAL, CHILD_HEALTH, SRH
If it fits multiple categories, pick the PRIMARY one.

Examples of classification:
- Pregnant woman with eclampsia → YES|MATERNAL
- 10-day-old baby with fever and jaundice → YES|NEONATAL
- 5-year-old with pneumonia → YES|CHILD_HEALTH
- Woman seeking family planning advice → YES|SRH
- 45-year-old man with chest pain → NO|NONE

Return EXACTLY {n} lines, one per scenario, in the same order. No extra text.

{scenarios}
"""


def classify_batch(model, batch_df, max_retries=3):
    """Classify a batch of vignettes using Gemini."""
    scenario_lines = []
    for _, row in batch_df.iterrows():
        scenario_text = str(row["User Prompt"])[:500]
        scenario_lines.append(f"[{row['StudyID']}]: {scenario_text}")

    scenarios_block = "\n\n".join(scenario_lines)
    prompt = BATCH_CLASSIFICATION_PROMPT.format(
        n=len(batch_df), scenarios=scenarios_block
    )

    for attempt in range(max_retries):
        try:
            response = model.generate_content(prompt)
            text = response.text.strip()

            results = {}
            for line in text.split("\n"):
                line = line.strip().upper()
                if not line:
                    continue
                match = re.match(r"^(\d+)\|(YES|NO)\|(\w+)", line)
                if match:
                    sid = int(match.group(1))
                    results[sid] = (match.group(2), match.group(3))

            output = []
            for _, row in batch_df.iterrows():
                sid = row["StudyID"]
                if sid in results:
                    output.append(results[sid])
                else:
                    output.append(("ERROR", "PARSE_FAIL"))
            return output

        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(2**attempt)
            else:
                print(f"  Batch error: {e}")
                return [("ERROR", "ERROR")] * len(batch_df)


def clean_text(text):
    """Remove \\r\\n and strip whitespace."""
    if pd.isna(text):
        return text
    return str(text).replace("\r", " ").replace("\n", " ").strip()


def main():
    # ── Load data ──────────────────────────────────────────────
    print("Loading data...")
    responses = pd.read_excel(RESPONSES_FILE)
    print(f"  Vignettes: {len(responses)}")

    # ── Configure Gemini ───────────────────────────────────────
    if not GEMINI_API_KEY:
        raise ValueError(
            "Set GEMINI_API_KEY as an environment variable or paste it in the script."
        )
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel(GEMINI_MODEL)

    # ── Classify all vignettes in batches ──────────────────────
    print(f"\nClassifying {len(responses)} vignettes (batch size {BATCH_SIZE})...")
    classifications = []
    n_batches = (len(responses) + BATCH_SIZE - 1) // BATCH_SIZE

    for b in range(n_batches):
        batch = responses.iloc[b * BATCH_SIZE : (b + 1) * BATCH_SIZE]
        results = classify_batch(model, batch)
        for (_, row), (decision, category) in zip(batch.iterrows(), results):
            classifications.append(
                {"StudyID": row["StudyID"], "decision": decision, "category": category}
            )
        print(f"  Batch {b + 1}/{n_batches} done ({len(classifications)} classified)")
        time.sleep(RATE_LIMIT_SECONDS)

    clf_df = pd.DataFrame(classifications)

    # ── Report classification results ──────────────────────────
    print(f"\nClassification results:")
    print(clf_df["decision"].value_counts().to_string())
    print()
    print(clf_df["category"].value_counts().to_string())

    errors = clf_df[clf_df["decision"] == "ERROR"]
    if len(errors) > 0:
        print(f"\n⚠ {len(errors)} classification errors — review these StudyIDs:")
        print(errors["StudyID"].tolist())

    # ── Filter to OBGYN/MCH/SRH ───────────────────────────────
    final_clf = clf_df[clf_df["decision"] == "YES"].copy()
    final_ids = final_clf["StudyID"].tolist()
    print(f"\nFinal set: {len(final_clf)} / {len(responses)} vignettes")
    print("Category breakdown:")
    for cat, count in final_clf["category"].value_counts().items():
        print(f"  {cat}: {count}")

    # ── Extract QA pairs ───────────────────────────────────────
    DATA_DIR.mkdir(exist_ok=True)
    vignettes = responses[responses["StudyID"].isin(final_ids)].merge(
        final_clf[["StudyID", "category"]], on="StudyID"
    )

    obgyn_qa = vignettes[
        ["StudyID", "User Prompt", "Clinician response", "category"]
    ].copy()
    obgyn_qa.columns = ["study_id", "scenario", "clinician_response", "category"]
    obgyn_qa["scenario"] = obgyn_qa["scenario"].apply(clean_text)
    obgyn_qa["clinician_response"] = obgyn_qa["clinician_response"].apply(clean_text)
    obgyn_qa = obgyn_qa.sort_values("study_id").reset_index(drop=True)

    obgyn_qa.to_csv(DATA_DIR / "obgyn_vignettes.tsv", sep="\t", index=False)
    print(f"Saved {len(obgyn_qa)} vignettes to data/obgyn_vignettes.tsv")

    # ── Summary ────────────────────────────────────────────────
    print("\n" + "=" * 60)
    print("EXTRACTION COMPLETE")
    print("=" * 60)
    print(f"Source: {len(responses)} vignettes")
    print(f"Extracted: {len(final_clf)} OBGYN/MCH/SRH vignettes")
    print(f"\nOutput: {DATA_DIR / 'obgyn_vignettes.tsv'} ({len(obgyn_qa)} rows)")


if __name__ == "__main__":
    main()
