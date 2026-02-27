"""
Extract OBGYN Questions from MedQA USMLE Dataset (Gemini API)

Classifies all 14,369 USMLE questions using Gemini API calls (100 per request),
then extracts those related to obstetrics & gynecology.

Source: Jin et al., 2020 — MedQA (arXiv:2009.13081)

Usage:
    python extract_obgyn_usmle.py                  # Run all (resumable)
    python extract_obgyn_usmle.py --limit 10       # Test with 10 questions

Requires:
    - GEMINI_API_KEY environment variable
    - pip install google-genai pandas
"""

import argparse
import json
import os
import re
import sys
import time
from pathlib import Path

# ============================================================
# CONFIGURATION
# ============================================================
GEMINI_MODEL = "gemini-3-flash-preview"
CHUNK_SIZE = 100  # questions per API call

SCRIPT_DIR = Path(__file__).parent
SOURCE_FILE = SCRIPT_DIR / "data_clean" / "questions" / "US" / "US_qbank.jsonl"
PROGRESS_FILE = SCRIPT_DIR / "classifications.jsonl"
DATA_DIR = SCRIPT_DIR / "data"
OUTPUT_FILE = DATA_DIR / "obgyn_usmle.tsv"

# ============================================================
# CLASSIFICATION PROMPT
# ============================================================
SYSTEM_PROMPT = """\
You are a medical specialty classifier. You will receive a numbered list of \
USMLE-style clinical questions. For EACH question, determine whether it \
primarily belongs to Obstetrics & Gynecology (OBGYN).

Classify each into ONE category:

- OBSTETRICS: pregnancy, labor, delivery, postpartum care, prenatal screening, \
fetal development, obstetric complications (preeclampsia, ectopic pregnancy, \
placenta previa, gestational diabetes, HELLP, etc.)
- GYNECOLOGY: menstrual disorders, PCOS, endometriosis, fibroids, pelvic \
inflammatory disease, ovarian/cervical/uterine pathology, gynecologic oncology, \
pelvic floor disorders, vulvovaginal conditions
- REPRODUCTIVE_HEALTH: contraception, family planning, infertility, assisted \
reproduction, menopause, hormone replacement therapy, STIs in reproductive context
- NONE: not primarily an OBGYN question. Even if the patient is female or \
pregnant, if the core medical concept being tested is from another specialty \
(e.g. a pregnant woman with a UTI testing antibiotic knowledge, or a woman \
with chest pain testing cardiology), classify as NONE.

Respond with a JSON array, one object per question in order:
[{"id": 0, "is_obgyn": true/false, "category": "..."}, ...]\
"""


def get_client():
    """Create a Gemini API client."""
    from google import genai

    api_key = os.environ.get("GEMINI_API_KEY", "")
    if not api_key:
        sys.exit("Error: Set GEMINI_API_KEY environment variable.")
    return genai.Client(api_key=api_key)


def load_questions():
    """Load USMLE questions from source JSONL."""
    questions = []
    with open(SOURCE_FILE) as f:
        for line in f:
            questions.append(json.loads(line))
    return questions


def load_progress():
    """Load already-classified question indices from progress file."""
    done = {}
    if PROGRESS_FILE.exists():
        with open(PROGRESS_FILE) as f:
            for line in f:
                if line.strip():
                    rec = json.loads(line)
                    done[rec["idx"]] = rec
    return done


def classify_chunk(client, chunk):
    """Classify a list of (global_idx, question_dict) pairs in one API call."""
    from google.genai import types

    # Build numbered question list
    parts = []
    for local_id, (_, q) in enumerate(chunk):
        opts = " | ".join(f"{k}. {v}" for k, v in q["options"].items())
        parts.append(f"[{local_id}] {q['question']}\nOptions: {opts}")

    user_text = "\n\n".join(parts)

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=user_text,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            temperature=0,
        ),
    )

    text = response.text.strip()
    # Strip markdown fences if present
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)

    results = json.loads(text)

    # Map back to global indices
    classified = {}
    for local_id, (global_idx, _) in enumerate(chunk):
        if local_id < len(results):
            clf = results[local_id]
            classified[global_idx] = {
                "is_obgyn": clf.get("is_obgyn", False),
                "category": clf.get("category", "NONE"),
            }
        else:
            classified[global_idx] = {"is_obgyn": False, "category": "ERROR"}

    return classified


def main():
    parser = argparse.ArgumentParser(
        description="Extract OBGYN questions from MedQA USMLE using Gemini API"
    )
    parser.add_argument("--limit", type=int, help="Only classify first N questions")
    args = parser.parse_args()

    import pandas as pd

    questions = load_questions()
    if args.limit:
        questions = questions[: args.limit]
        print(f"Limited to {len(questions)} questions (test mode)")
    else:
        print(f"Loaded {len(questions)} questions")

    # ── Load progress (resumable) ─────────────────────────────
    done = load_progress()
    print(f"Already classified: {len(done)}/{len(questions)}")

    # Build list of (global_idx, question) pairs still to do
    todo = [(i, q) for i, q in enumerate(questions) if i not in done]

    if not todo:
        print("All questions already classified. Skipping to TSV export.")
    else:
        # Split into chunks
        chunks = [todo[i:i + CHUNK_SIZE] for i in range(0, len(todo), CHUNK_SIZE)]
        print(f"Classifying {len(todo)} questions in {len(chunks)} chunks of up to {CHUNK_SIZE}...\n")

        client = get_client()

        with open(PROGRESS_FILE, "a") as pf:
            for chunk_num, chunk in enumerate(chunks, 1):
                idx_range = f"q-{chunk[0][0]}..q-{chunk[-1][0]}"

                # Retry with backoff on rate limit errors
                for attempt in range(5):
                    try:
                        classified = classify_chunk(client, chunk)
                        break
                    except Exception as e:
                        err_str = str(e)
                        if "429" in err_str or "RESOURCE_EXHAUSTED" in err_str:
                            wait = 30 * (attempt + 1)
                            print(f"  Rate limited on chunk {chunk_num}, waiting {wait}s...")
                            time.sleep(wait)
                        else:
                            print(f"  Error on chunk {chunk_num} ({idx_range}): {e}")
                            classified = {
                                idx: {"is_obgyn": False, "category": "ERROR"}
                                for idx, _ in chunk
                            }
                            break
                else:
                    print(f"  Giving up on chunk {chunk_num} after 5 retries")
                    classified = {
                        idx: {"is_obgyn": False, "category": "ERROR"}
                        for idx, _ in chunk
                    }

                # Save progress immediately
                for global_idx, clf in classified.items():
                    rec = {"idx": global_idx, **clf}
                    pf.write(json.dumps(rec) + "\n")
                    done[global_idx] = rec
                pf.flush()

                obgyn_in_chunk = sum(1 for c in classified.values() if c.get("is_obgyn"))
                print(f"  [{chunk_num}/{len(chunks)}] {idx_range}: "
                      f"{len(classified)} classified, {obgyn_in_chunk} OBGYN")

    # ── Build TSV from progress file ─────────────────────────
    print("\nBuilding TSV...")
    done = load_progress()

    obgyn_rows = []
    category_counts = {}
    for i, q in enumerate(questions):
        clf = done.get(i, {"is_obgyn": False, "category": "NONE"})

        is_obgyn = clf.get("is_obgyn", False)
        category = clf.get("category", "NONE")
        category_counts[category] = category_counts.get(category, 0) + 1

        if is_obgyn and category != "NONE":
            opts = " | ".join(f"{k}. {v}" for k, v in q["options"].items())
            correct_letter = q["answer"]
            answer_text = q.get("options", {}).get(correct_letter, "")
            obgyn_rows.append(
                {
                    "question": q["question"],
                    "options_formatted": opts,
                    "correct_letter": correct_letter,
                    "answer": answer_text,
                    "category": category,
                    "meta_info": q.get("meta_info", ""),
                }
            )

    print(f"\nClassification breakdown ({len(questions)} total):")
    for cat, count in sorted(category_counts.items(), key=lambda x: -x[1]):
        print(f"  {cat}: {count}")

    DATA_DIR.mkdir(exist_ok=True)
    df = pd.DataFrame(obgyn_rows)

    if not df.empty:
        for col in df.columns:
            df[col] = df[col].apply(
                lambda x: str(x)
                .replace("\r\n", "\\n")
                .replace("\r", "\\n")
                .replace("\n", "\\n")
                .strip()
                if pd.notna(x)
                else x
            )

    df.to_csv(OUTPUT_FILE, sep="\t", index=False)

    print(f"\n{'=' * 60}")
    print("EXTRACTION COMPLETE")
    print(f"{'=' * 60}")
    print(f"Source: {len(questions)} USMLE questions")
    print(f"Extracted: {len(df)} OBGYN questions")
    print(f"Output: {OUTPUT_FILE}")
    if not df.empty:
        print(f"\nCategory breakdown:")
        for cat, count in df["category"].value_counts().items():
            print(f"  {cat}: {count}")


if __name__ == "__main__":
    main()
