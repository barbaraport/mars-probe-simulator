import uuid

from sqlalchemy import UUID, CheckConstraint, Enum, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.Base import Base
from app.schemas.direction import Direction


class Probe(Base):
    __tablename__ = "probe"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    x: Mapped[int] = mapped_column(Integer, nullable=False)
    y: Mapped[int] = mapped_column(Integer, nullable=False)
    direction: Mapped[Direction] = mapped_column(
        Enum(Direction, name="direction"), nullable=False
    )

    grid: Mapped["Grid"] = relationship(  # type: ignore  # noqa: F821
        "Grid", back_populates="probe", uselist=False, lazy="selectin"
    )

    __table_args__ = (
        CheckConstraint("x >= 0", name="check_valid_probe_x_position"),
        CheckConstraint("y >= 0", name="check_valid_probe_y_position"),
    )
