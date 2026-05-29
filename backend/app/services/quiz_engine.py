import random

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.user_competency import UserCompetency
from app.db.models.question import Question


def get_weak_competencies(db: Session, user_id: str, limit: int = 5):
    stmt = (
        select(UserCompetency)
        .where(UserCompetency.user_id == user_id)
        .order_by(UserCompetency.weakness_score.desc())
        .limit(limit)
    )

    return db.scalars(stmt).all()


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

    # naive shuffle + cap
    random.shuffle(questions)

    return questions[:limit]
