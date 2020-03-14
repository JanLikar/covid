from sqlalchemy import (
    func,
    Column,
    DateTime,
    Integer,
    Text,
)

from .meta import Base


class Comment(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True)
    email = Column(Text, nullable=False)
    name = Column(Text, nullable=False)
    comment = Column(Text(), nullable=False)
    created = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    marker_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=True)
