import uuid

from sqlalchemy import (
    String,
    Text,
    Integer,
    Boolean,
    ForeignKey,
    DateTime,
    func,
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Question(Base):
    __tablename__ = "questions"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    competency_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("competencies.id"),
        nullable=False,
    )

    question_type: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    difficulty: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    prompt: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    correct_answer: Mapped[str | None] = mapped_column(Text)

    acceptable_answers: Mapped[list] = mapped_column(
        JSONB,
        default=list,
    )

    explanation: Mapped[str | None] = mapped_column(Text)

    metadata_json: Mapped[dict] = mapped_column(
        JSONB,
        default=dict,
    )
    source: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    times_used: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    competency = relationship(
        "Competency",
        back_populates="questions",
    )
