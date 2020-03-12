from sqlalchemy import (
    func,
    Column,
    Date,
    DateTime,
    Index,
    Integer,
    Numeric,
    Text,
    Boolean
)

from .meta import Base


class Marker(Base):
    __tablename__ = 'markers'
    id = Column(Integer, primary_key=True)
    longitude = Column(Numeric, nullable=False)
    latitude = Column(Numeric, nullable=False)
    name = Column(Text, nullable=False)
    note = Column(Text, default='', nullable=False)
    reported_date = Column(Date, nullable=False)
    created = Column(DateTime(timezone=True),
                     default=func.now(), nullable=False)
    updated = Column(DateTime(timezone=True), default=func.now(),
                     onupdate=func.now(), nullable=False)
    user_id = Column(Integer, default=0, nullable=False)
    deleted = Column(Boolean(name='deleted_ck'), default=False)
