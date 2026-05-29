import uuid

from sqlalchemy import (
    ForeignKey,
    Text,
    Numeric,
    DateTime,
    func,
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class EssaySubmission(Base):
    __tablename__ = "essay_submissions"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    competency_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("competencies.id"),
    )

    prompt: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    submission: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    overall_score: Mapped[float | None] = mapped_column(
        Numeric(5, 2)
    )

    grammar_score: Mapped[float | None] = mapped_column(
        Numeric(5, 2)
    )

    naturalness_score: Mapped[float | None] = mapped_column(
        Numeric(5, 2)
    )

    vocabulary_score: Mapped[float | None] = mapped_column(
        Numeric(5, 2)
    )

    coherence_score: Mapped[float | None] = mapped_column(
        Numeric(5, 2)
    )

    feedback: Mapped[dict] = mapped_column(
        JSONB,
        default=dict,
    )

    corrected_version: Mapped[str | None] = mapped_column(
        Text
    )

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
