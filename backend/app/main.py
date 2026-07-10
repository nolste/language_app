from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from fastapi import FastAPI, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session


from app.db.models.competency import Competency
from app.db.base import Base
from app.db.session import engine, get_db
from app.db.models import user, competency, question  # noqa
from app.api.quiz import router as quiz_router

app = FastAPI(title="Portuguese Competency API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Next.js dev server
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(quiz_router)


@app.get("/")
def healthcheck():
    return {"status": "ok"}


@app.get("/competencies")
def get_competencies(
    db: Session = Depends(get_db)
):
    competencies = db.scalars(
        select(Competency).order_by(
            Competency.recommended_order
        )
    ).all()

    return competencies
