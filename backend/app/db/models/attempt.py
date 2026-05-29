import uuid

from sqlalchemy import (
    ForeignKey,
    Text,
    Integer,
    Numeric,
    DateTime,
    func,
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Attempt(Base):
    __tablename__ = "attempts"

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

    question_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("questions.id", ondelete="CASCADE"),
        nullable=False,
    )

    submitted_answer: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    score: Mapped[float] = mapped_column(
        Numeric(5, 2),
        nullable=False,
    )

    response_time_seconds: Mapped[int | None] = mapped_column(
        Integer
    )

    llm_feedback: Mapped[dict] = mapped_column(
        JSONB,
        default=dict,
    )

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    user = relationship(
        "User",
        back_populates="attempts",
    )

    question = relationship(
        "Question",
    )
