import uuid
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.db.models.competency import Competency


COMPETENCIES = [
    # CORE GRAMMAR
    ("definite_indefinite_articles", "Definite/Indefinite Articles", "grammar", 2, 1),
    ("noun_gender_patterns", "Noun Gender Patterns", "grammar", 2, 2),
    ("plural_formation_irregular", "Irregular Plural Formation", "grammar", 2, 3),
    ("adjective_noun_agreement", "Adjective-Noun Agreement", "grammar", 2, 4),
    ("quantifiers_muito_pouco_demais", "Quantifiers", "grammar", 2, 5),

    # PRONOUNS
    ("object_pronouns_direct_indirect",
     "Direct & Indirect Object Pronouns", "grammar", 3, 1),
    ("reflexive_verbs", "Reflexive Verbs", "grammar", 3, 2),

    # PREPOSITIONS
    ("preposition_de_usage", "Preposition De Usage", "grammar", 3, 3),
    ("preposition_em_vs_a", "Preposition Em vs A", "grammar", 3, 4),
    ("preposition_com_sem_emphasized_meaning",
     "Prepositions Com vs Sem", "grammar", 3, 5),

    # VERB TENSES
    ("future_do_present", "Future do Presente", "verb_tense", 3, 1),
    ("future_do_past", "Future do Passado", "verb_tense", 3, 2),
    ("subjunctive_imperfect", "Subjunctive Imperfect", "verb_tense", 4, 3),
    ("subjunctive_future", "Subjunctive Future", "verb_tense", 4, 4),

    # SYNTAX
    ("relative_clauses", "Relative Clauses", "grammar", 3, 6),
    ("negation_structures", "Negation Structures", "grammar", 2, 7),
    ("question_formation_inversion", "Question Formation & Inversion", "grammar", 2, 8),

    # USAGE DISTINCTIONS
    ("haver_vs_ter_existential", "Haver vs Ter", "grammar", 3, 9),
    ("saber_vs_conhecer", "Saber vs Conhecer", "grammar", 3, 10),
    ("levar_trazer", "Levar vs Trazer", "grammar", 3, 11),
]


def seed():
    db: Session = SessionLocal()

    existing = {
        row[0]
        for row in db.query(Competency.slug).all()
    }

    inserted = 0

    for slug, name, category, difficulty_level, order in COMPETENCIES:
        if slug in existing:
            continue

        competency = Competency(
            id=uuid.uuid4(),
            slug=slug,
            name=name,
            category=category,
            description=None,
            parent_id=None,
            difficulty_level=difficulty_level,
            recommended_order=order,
            is_active=True,
            metadata_json={},
        )

        db.add(competency)
        inserted += 1

    db.commit()
    db.close()

    print(f"Seed complete. Inserted {inserted} competencies.")


if __name__ == "__main__":
    seed()
