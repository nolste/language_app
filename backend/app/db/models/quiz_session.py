import uuid
from datetime import datetime

from sqlalchemy import ForeignKey, DateTime, func, Integer
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class QuizSession(Base):
    __tablename__ = "quiz_sessions"

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

    total_questions: Mapped[int] = mapped_column(Integer, default=0)

    status: Mapped[str] = mapped_column(
        default="active"
    )  # active | completed

    questions_snapshot: Mapped[dict] = mapped_column(
        JSONB,
        default=dict,
    )

    results: Mapped[dict] = mapped_column(
        JSONB,
        default=dict,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    user = relationship("User")
