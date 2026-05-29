from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Dict

from app.db.models.attempt import Attempt
from app.services.grading import grade_answer
from app.services.progress import update_user_competency
from app.db.session import get_db
from app.services.quiz_engine import (
    get_weak_competencies,
    get_questions_for_competencies,
)
from app.db.models.question import Question
from backend.helper_functions.helper import is_valid_uuid

router = APIRouter(prefix="/quiz", tags=["quiz"])


class QuizStartRequest(BaseModel):
    user_id: str
    num_questions: int = 15


class QuizSubmitRequest(BaseModel):
    user_id: str
    answers: Dict[str, str]  # question_id -> answer


@router.post("/start")
def start_quiz(
    payload: QuizStartRequest,
    db: Session = Depends(get_db),
):
    weak = get_weak_competencies(db, payload.user_id)

    competency_ids = [w.competency_id for w in weak]

    questions = get_questions_for_competencies(
        db,
        competency_ids,
        limit=payload.num_questions,
    )

    return {
        "user_id": payload.user_id,
        "weak_competencies": [
            {
                "competency_id": w.competency_id,
                "weakness_score": float(w.weakness_score),
                "mastery_score": float(w.mastery_score),
            }
            for w in weak
        ],
        "questions": [
            {
                "id": str(q.id),
                "competency_id": q.competency_id,
                "prompt": q.prompt,
                "question_type": q.question_type,
                "metadata": q.metadata_json,
            }
            for q in questions
        ],
    }


@router.post("/submit")
def submit_quiz(
    payload: QuizSubmitRequest,
    db: Session = Depends(get_db),
):
    results = []

    for question_id, answer in payload.answers.items():
        if not is_valid_uuid(question_id):
            continue

        question = db.get(Question, question_id)
        if not question:
            continue

        score, is_correct, feedback = grade_answer(
            question,
            answer,
        )

        attempt = Attempt(
            user_id=payload.user_id,
            question_id=question_id,
            submitted_answer=answer,
            score=score,
            llm_feedback=feedback,
        )

        db.add(attempt)

        uc = update_user_competency(
            db,
            payload.user_id,
            str(question.competency_id),
            is_correct,
        )

        results.append(
            {
                "question_id": question_id,
                "score": score,
                "is_correct": is_correct,
                "competency": str(question.competency_id),
                "new_mastery": float(uc.mastery_score),
                "new_weakness": float(uc.weakness_score),
            }
        )

    db.commit()

    return {
        "results": results
    }
