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
    longitude = Column(Numeric)
    latitude = Column(Numeric)
    name = Column(Text(length=50))
    note = Column(Text(length=500), default='')
    reported_date = Column(Date)
    created = Column(DateTime(timezone=True), default=func.now())
    updated = Column(DateTime(timezone=True), onupdate=func.now())
