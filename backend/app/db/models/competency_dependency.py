import uuid

from sqlalchemy import (
    ForeignKey,
    Numeric,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class CompetencyDependency(Base):
    __tablename__ = "competency_dependencies"

    __table_args__ = (
        UniqueConstraint(
            "competency_id",
            "depends_on_id",
            name="uq_competency_dependency",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    competency_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(
            "competencies.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    depends_on_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(
            "competencies.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    minimum_mastery: Mapped[float] = mapped_column(
        Numeric(5, 2),
        default=0.70,
    )
