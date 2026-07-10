import random
import uuid
from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.db.models.question import Question
from app.db.models.quiz_session import QuizSession
from app.db.models.user_competency import UserCompetency


# -----------------------------
# Core signal: weak competencies
# -----------------------------
def get_weak_competencies(db: Session, user_id: str, limit: int = 5):
    stmt = (
        select(UserCompetency)
        .where(UserCompetency.user_id == user_id)
        .order_by(UserCompetency.weakness_score.desc())
        .limit(limit)
    )
    return db.scalars(stmt).all()


# -----------------------------
# Question retrieval (adaptive path)
# -----------------------------
def get_questions_for_competencies(
    db: Session,
    competency_ids: list,
    limit: int = 15,
):
    stmt = (
        select(Question)
        .where(Question.competency_id.in_(competency_ids))
        .where(Question.is_active == True)
    )

    questions = list(db.scalars(stmt).all())
    random.shuffle(questions)

    return questions[:limit]


# -----------------------------
# Fallback pool (cold start)
# -----------------------------
def get_fallback_questions(db: Session, limit: int):
    stmt = (
        select(Question)
        .where(Question.is_active == True)
        .order_by(func.random())
        .limit(limit)
    )

    return list(db.scalars(stmt).all())


# -----------------------------
# MAIN ENGINE ENTRYPOINT
# -----------------------------
def create_quiz_session(
    db: Session,
    user_id: str,
    num_questions: int = 15,
    adaptive_threshold: int = 3,
):
    """
    Single entrypoint for quiz generation.
    Decides adaptive vs fallback automatically.
    """

    weak = get_weak_competencies(db, user_id, limit=10)

    use_adaptive = len(weak) >= adaptive_threshold

    if use_adaptive:
        competency_ids = [w.competency_id for w in weak]
        questions = get_questions_for_competencies(
            db,
            competency_ids,
            limit=num_questions,
        )
    else:
        questions = get_fallback_questions(db, num_questions)

    # -----------------------------
    # Create session snapshot
    # -----------------------------
    session = QuizSession(
        id=uuid.uuid4(),
        user_id=user_id,
        total_questions=len(questions),
        questions_snapshot={
            str(q.id): {
                "competency_id": str(q.competency_id),
                "prompt": q.prompt,
                "question_type": q.question_type,
                "correct_answer": q.correct_answer,
            }
            for q in questions
        },
        status="active",
    )

    db.add(session)
    db.commit()
    db.refresh(session)

    return session, questions
