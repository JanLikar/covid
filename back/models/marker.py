from sqlalchemy import (
    func,
    Column,
    Date,
    DateTime,
    Index,
    Integer,
    Numeric,
    Text,
)

from .meta import Base


class Marker(Base):
    __tablename__ = 'markers'
    id = Column(Integer, primary_key=True)
    longitude = Column(Numeric, nullable=False)
    latitude = Column(Numeric, nullable=False)
    name = Column(Text(length=50), nullable=False)
    note = Column(Text(length=500), default='', nullable=False)
    reported_date = Column(Date, nullable=False)
    created = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    updated = Column(DateTime(timezone=True), onupdate=func.now(), nullable=False)
