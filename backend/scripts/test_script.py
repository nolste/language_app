# scripts/reset_questions.py

from app.db.session import SessionLocal
from app.db.models.question import Question


def run():
    db = SessionLocal()

    deleted = db.query(Question).delete()

    db.commit()

    print(f"Deleted {deleted} questions")


if __name__ == "__main__":
    run()
