import uuid
from datetime import datetime

from sqlalchemy import (
    ForeignKey,
    Integer,
    Numeric,
    DateTime,
    func,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class UserCompetency(Base):
    __tablename__ = "user_competencies"

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "competency_id",
            name="uq_user_competency",
        ),
    )

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

    competency_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("competencies.id", ondelete="CASCADE"),
        nullable=False,
    )

    mastery_score: Mapped[float] = mapped_column(
        Numeric(5, 2),
        default=0,
    )

    confidence_score: Mapped[float] = mapped_column(
        Numeric(5, 2),
        default=0,
    )

    weakness_score: Mapped[float] = mapped_column(
        Numeric(5, 2),
        default=1,
    )

    attempt_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    correct_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    streak: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    last_reviewed_at: Mapped[datetime | None]

    next_review_at: Mapped[datetime | None]

    metadata_json: Mapped[dict] = mapped_column(
        JSONB,
        default=dict,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )
