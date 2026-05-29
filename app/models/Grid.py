import uuid

from sqlalchemy import UUID, CheckConstraint, Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.models.Base import Base


class Grid(Base):
    __tablename__ = "grid"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    x = Column(Integer, nullable=False)
    y = Column(Integer, nullable=False)
    probe_id=Column(UUID(as_uuid=True), ForeignKey("probe.id"), default=uuid.uuid4)
    probe = relationship("Probe", back_populates="grid")

    __table_args__ = (
        CheckConstraint("x >= 0", name="check_valid_grid_x_position"),
        CheckConstraint("y >= 0", name="check_valid_grid_y_position"),
    )
