import json
import uuid
import os
import hashlib
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.db.models.competency import Competency
from app.db.models.question import Question
from openai import OpenAI
from dotenv import load_dotenv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_FILE = BASE_DIR / ".env"

load_dotenv(ENV_FILE)

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("OPENAI_API_KEY not found in environment")

client = OpenAI(api_key=api_key)

MODEL = "gpt-5"
TARGET_QUESTIONS_PER_COMPETENCY = 40


# ----------------------------
# Helpers
# ----------------------------

def make_hash(competency_id: str, prompt: str) -> str:
    raw = f"{competency_id}:{prompt.strip().lower()}"
    return hashlib.md5(raw.encode()).hexdigest()


def build_prompt(comp: Competency, n: int) -> str:
    return f"""
Generate {n} Portuguese learning questions.

Competency:
Name: {comp.name}
Slug: {comp.slug}

Target audience:
Intermediate to advanced Portuguese learners.

Question distribution:
- 30% fill_blank
- 30% multiple_choice
- 20% translation
- 20% error_correction

Rules:
- Use natural Brazilian Portuguese.
- Use realistic sentences.
- Avoid textbook-style fragments.
- Avoid duplicate questions.
- Difficulty should range from 2-5.
- Every question must have an explanation That explanation should be in english.

IMPORTANT:

For multiple_choice:
- metadata.choices must contain the answer options.
- correct_answer must contain the ACTUAL answer text.
- Never use A/B/C/D as the correct answer.

Example:

{{
  "question_type": "multiple_choice",
  "prompt": "Complete...",
  "correct_answer": "por que",
  "metadata": {{
    "choices": [
      "por que",
      "porque",
      "porquê",
      "por quê"
    ]
  }}
}}

For fill_blank:
- Always include a hint.
- Hint must be stored in metadata.
- Use one of:

metadata:
{{
  "question_subtype": "verb_conjugation",
  "hint_type": "infinitive",
  "hint": "fazer"
}}

OR

metadata:
{{
  "question_subtype": "vocabulary",
  "hint_type": "english",
  "hint": "to achieve"
}}

For translation:
- question_type = "translation"
- metadata.direction must be:
  - en_to_pt
  - pt_to_en

For error_correction:
- prompt contains an incorrect sentence.
- correct_answer contains the corrected sentence.

The explanation should be in english

Return ONLY valid JSON.

Schema:

[
  {{
    "prompt": "...",
    "question_type": "...",
    "correct_answer": "...",
    "acceptable_answers": [],
    "difficulty": 3,
    "explanation": "...",
    "metadata": {{
      "question_subtype": "...",
      "hint_type": "...",
      "hint": "...",
      "choices": [],
      "direction": "..."
    }}
  }}
]

No markdown.
No code fences.
JSON only.
"""


def generate_questions(comp: Competency, n: int):
    prompt = build_prompt(comp, n)

    response = client.responses.create(
        model=MODEL,
        input=prompt,
    )

    text = response.output_text

    try:
        cleaned = text.strip()

        # remove markdown fences
        if cleaned.startswith("```"):
            cleaned = cleaned.replace("```json", "")
            cleaned = cleaned.replace("```", "")
            cleaned = cleaned.strip()

        # find first JSON array
        start = cleaned.find("[")
        end = cleaned.rfind("]")

        if start == -1 or end == -1:
            raise ValueError("No JSON array found")

        cleaned = cleaned[start: end + 1]

        questions = json.loads(cleaned)

        if not isinstance(questions, list):
            raise ValueError("Response is not a list")

        return questions

    except Exception as e:
        print(f"\n[ERROR parsing JSON] competency={comp.slug}")
        print(f"Error: {e}")
        print(text[:2000])

        return []


def validate_question(q: dict) -> bool:

    if not q.get("prompt"):
        return False

    if not q.get("question_type"):
        return False

    if q["question_type"] == "multiple_choice":
        choices = q.get("metadata", {}).get("choices", [])

        if len(choices) < 2:
            return False

        if q.get("correct_answer") not in choices:
            return False

    if q["question_type"] == "fill_blank":
        metadata = q.get("metadata", {})

        if "hint" not in metadata:
            return False

    return True
# ----------------------------
# Main generation logic
# ----------------------------


def run():
    db: Session = SessionLocal()

    competencies = db.query(Competency).filter(
        Competency.is_active == True
    ).all()

    total_created = 0

    for comp in competencies:

        existing_count = db.query(Question).filter(
            Question.competency_id == comp.id
        ).count()

        to_create = TARGET_QUESTIONS_PER_COMPETENCY - existing_count

        if to_create <= 0:
            continue

        print(f"\nGenerating {to_create} questions for: {comp.slug}")

        questions = generate_questions(comp, to_create)

        created_this_comp = 0

        for q in questions:
            if not validate_question(q) or not q.get("prompt"):
                continue

            h = make_hash(str(comp.id), q["prompt"])

            # duplicate check
            exists = db.query(Question).filter(
                Question.metadata_json["hash"].astext == h
            ).first()

            if exists:
                continue

            question = Question(
                id=uuid.uuid4(),
                competency_id=comp.id,
                prompt=q["prompt"],
                question_type=q["question_type"],
                correct_answer=q.get("correct_answer"),
                acceptable_answers=q.get("acceptable_answers", []),
                explanation=q.get("explanation"),
                difficulty=q.get("difficulty", 3),
                source="ai_generated",
                is_active=True,
                metadata_json={
                    **q.get("metadata", {}),
                    "hash": h,
                    "model": MODEL,
                    "competency_slug": comp.slug,
                },
            )

            db.add(question)
            created_this_comp += 1
            total_created += 1

        db.commit()
        print(f"Created {created_this_comp} for {comp.slug}")

    print("\nDONE")
    print("Total questions created:", total_created)


if __name__ == "__main__":
    run()
