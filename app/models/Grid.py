import uuid

from sqlalchemy import UUID, CheckConstraint, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.Base import Base


class Grid(Base):
    __tablename__ = "grid"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    x: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    y: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    probe_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("probe.id"), unique=True, nullable=False
    )
    probe: Mapped["Probe"] = relationship("Probe", back_populates="grid")  # type: ignore  # noqa: F821

    __table_args__ = (
        CheckConstraint("x >= 0", name="check_valid_grid_x_position"),
        CheckConstraint("y >= 0", name="check_valid_grid_y_position"),
    )
