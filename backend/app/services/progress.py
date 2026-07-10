from sqlalchemy.orm import Session

from app.db.models.user_competency import UserCompetency


def update_user_competency(
    db: Session,
    user_id: str,
    competency_id: str,
    is_correct: bool,
):
    uc = (
        db.query(UserCompetency)
        .filter_by(
            user_id=user_id,
            competency_id=competency_id,
        )
        .first()
    )

    if not uc:
        uc = UserCompetency(
            user_id=user_id,
            competency_id=competency_id,
            mastery_score=0,
            weakness_score=1,
            attempt_count=0,
            correct_count=0,
        )
        db.add(uc)

    uc.attempt_count = (uc.attempt_count or 0) + 1

    if is_correct:
        uc.correct_count += 1
        uc.mastery_score += 0.05
        uc.weakness_score = max(0, uc.weakness_score - 0.05)
        uc.streak = (uc.streak or 0) + 1
    else:
        uc.mastery_score = max(0, uc.mastery_score - 0.03)
        uc.weakness_score += 0.07
        uc.streak = 0

    uc.mastery_score = min(1.0, uc.mastery_score)
    uc.weakness_score = min(1.0, uc.weakness_score)

    return uc
