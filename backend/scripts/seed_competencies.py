import uuid

from sqlalchemy import select

from app.db.session import SessionLocal
from app.db.models.competency import Competency


COMPETENCIES = [
    # Root
    {
        "slug": "grammar",
        "name": "Grammar",
        "category": "grammar",
        "parent_slug": None,
        "difficulty_level": 1,
        "recommended_order": 1,
    },

    # Verb tenses
    {
        "slug": "verb_tenses",
        "name": "Verb Tenses",
        "category": "verb_tense",
        "parent_slug": "grammar",
        "difficulty_level": 1,
        "recommended_order": 2,
    },
    {
        "slug": "present_tense",
        "name": "Present Tense",
        "category": "verb_tense",
        "parent_slug": "verb_tenses",
        "difficulty_level": 1,
        "recommended_order": 3,
    },
    {
        "slug": "preterito_perfeito",
        "name": "Pretérito Perfeito",
        "category": "verb_tense",
        "parent_slug": "verb_tenses",
        "difficulty_level": 2,
        "recommended_order": 4,
    },
    {
        "slug": "preterito_imperfeito",
        "name": "Pretérito Imperfeito",
        "category": "verb_tense",
        "parent_slug": "verb_tenses",
        "difficulty_level": 2,
        "recommended_order": 5,
    },
    {
        "slug": "perfeito_vs_imperfeito",
        "name": "Perfeito vs Imperfeito",
        "category": "verb_tense",
        "parent_slug": "verb_tenses",
        "difficulty_level": 3,
        "recommended_order": 6,
    },
    {
        "slug": "subjunctive_present",
        "name": "Present Subjunctive",
        "category": "verb_tense",
        "parent_slug": "verb_tenses",
        "difficulty_level": 4,
        "recommended_order": 7,
    },

    # Core grammar
    {
        "slug": "ser_vs_estar",
        "name": "Ser vs Estar",
        "category": "grammar",
        "parent_slug": "grammar",
        "difficulty_level": 2,
        "recommended_order": 8,
    },
    {
        "slug": "por_vs_para",
        "name": "Por vs Para",
        "category": "grammar",
        "parent_slug": "grammar",
        "difficulty_level": 3,
        "recommended_order": 9,
    },
    {
        "slug": "gender_agreement",
        "name": "Gender Agreement",
        "category": "grammar",
        "parent_slug": "grammar",
        "difficulty_level": 2,
        "recommended_order": 10,
    },
    {
        "slug": "natural_phrasing",
        "name": "Natural Phrasing",
        "category": "writing",
        "parent_slug": "grammar",
        "difficulty_level": 4,
        "recommended_order": 11,
    },
]


def seed():
    db = SessionLocal()

    try:
        competency_map = {}

        for item in COMPETENCIES:
            existing = db.scalar(
                select(Competency).where(
                    Competency.slug == item["slug"]
                )
            )

            if existing:
                competency_map[item["slug"]] = existing
                continue

            competency = Competency(
                id=uuid.uuid4(),
                slug=item["slug"],
                name=item["name"],
                category=item["category"],
                difficulty_level=item["difficulty_level"],
                recommended_order=item[
                    "recommended_order"
                ],
            )

            db.add(competency)
            db.flush()

            competency_map[item["slug"]] = competency

        for item in COMPETENCIES:
            if item["parent_slug"]:
                competency = competency_map[
                    item["slug"]
                ]
                parent = competency_map[
                    item["parent_slug"]
                ]

                competency.parent_id = parent.id

        db.commit()

        print("Seed complete")

    finally:
        db.close()


if __name__ == "__main__":
    seed()
