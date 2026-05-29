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


class Competency(Base):
    __tablename__ = "competencies"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    slug: Mapped[str] = mapped_column(
        String,
        unique=True,
        nullable=False,
    )

    name: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(Text)

    category: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    parent_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("competencies.id"),
    )

    difficulty_level: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    recommended_order: Mapped[int | None] = mapped_column(Integer)

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )

    metadata_json: Mapped[dict] = mapped_column(
        JSONB,
        default=dict,
    )
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    parent = relationship(
        "Competency",
        remote_side=[id],
    )

    questions = relationship(
        "Question",
        back_populates="competency",
    )
