import uuid

from sqlalchemy import UUID, CheckConstraint, Column, Enum, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.models.Base import Base
from app.models.Direction import Direction


class Probe(Base):
    __tablename__ = "probe"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    x = Column(Integer, nullable=False)
    y = Column(Integer, nullable=False)
    direction = Column(Enum(Direction, name="direction"), nullable=False)

    grid_id = Column(UUID(as_uuid=True), ForeignKey("grid.id"), default=uuid.uuid4)
    grid = relationship("Grid", back_populates="probe", uselist=False)

    __table_args__ = (
        CheckConstraint("x >= 0", name="check_valid_grid_x_position"),
        CheckConstraint("y >= 0", name="check_valid_grid_y_position"),
    )
