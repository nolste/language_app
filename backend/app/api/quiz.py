import uuid
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Dict, Any
from enum import Enum

from app.db.models.attempt import Attempt
from app.services.grading import grade_answer
from app.services.progress import update_user_competency
from app.db.session import get_db
from app.services.quiz_engine import (
    create_quiz_session
)
from app.db.models.quiz_session import QuizSession
from app.db.models.question import Question


router = APIRouter(prefix="/quiz", tags=["quiz"])


class QuizStatus(str, Enum):
    ACTIVE = "active"
    COMPLETED = "completed"


class QuizStartRequest(BaseModel):
    user_id: uuid.UUID
    num_questions: int = 15


class QuizSubmitRequest(BaseModel):
    session_id: uuid.UUID
    answers: Dict[uuid.UUID, str]  # question_id -> answer


def normalize_choices(choices):
    if not choices:
        return []

    # unwrap accidental nesting
    if isinstance(choices, list) and len(choices) == 1 and isinstance(choices[0], list):
        return choices[0]

    return choices


def serialize_question(q):
    base = {
        "id": str(q.id),
        "prompt": q.prompt,
        "question_type": q.question_type,
        "difficulty": q.difficulty,
        "hint": q.metadata_json.get("hint"),
        "hint_type": q.metadata_json.get("hint_type"),
    }

    if q.question_type == "multiple_choice":
        raw = q.metadata_json.get("choices", [])
        base["choices"] = normalize_choices(raw)

    elif q.question_type == "translation":
        base["direction"] = q.metadata_json.get("direction")

    elif q.question_type in ["fill_blank", "error_correction"]:
        base["acceptable_answers"] = q.acceptable_answers

    return base


@router.post("/start")
def start_quiz(payload: QuizStartRequest, db: Session = Depends(get_db)):

    session, questions = create_quiz_session(
        db=db,
        user_id=str(payload.user_id),
        num_questions=payload.num_questions,
    )

    return {
        "session_id": str(session.id),
        "questions": [serialize_question(q) for q in questions]
    }


@router.post("/submit")
def submit_quiz(
    payload: QuizSubmitRequest,
    db: Session = Depends(get_db),
):
    session = db.get(QuizSession, payload.session_id)

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    if session.status == QuizStatus.COMPLETED:
        raise HTTPException(
            status_code=400, detail="Session already completed")

    results = []
    total_score = 0

    try:
        for question_id, answer in payload.answers.items():

            question = db.get(Question, question_id)
            if not question:
                continue

            score, is_correct, feedback = grade_answer(
                question,
                answer,
            )

            attempt = Attempt(
                user_id=session.user_id,
                question_id=question_id,
                submitted_answer=answer,
                score=score,
                llm_feedback=feedback,
            )

            db.add(attempt)

            update_user_competency(
                db,
                str(session.user_id),
                str(question.competency_id),
                is_correct,
            )

            total_score += score

            results.append(
                {
                    "question_id": str(question_id),
                    "score": score,
                    "is_correct": is_correct,
                }
            )

        session.results = {
            "total_score": total_score,
            "results": results,
        }

        session.status = QuizStatus.COMPLETED
        session.completed_at = datetime.now(timezone.utc)

        db.commit()

    except Exception:
        db.rollback()
        raise

    return {
        "session_id": session.id,
        "total_score": total_score,
        "results": results,
    }
