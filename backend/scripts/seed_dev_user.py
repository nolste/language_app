# scripts/seed_dev_user.py

import uuid
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.db.models.user import User


def run():
    db: Session = SessionLocal()

    user_id = uuid.uuid4()

    user = User(
        id=user_id,
        email="dev@test.com",
        name="Dev User"
    )

    db.add(user)
    db.commit()

    print("DEV USER ID:", user_id)


if __name__ == "__main__":
    run()
