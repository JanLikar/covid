from sqlalchemy import (
    func,
    Column,
    Integer,
    Text,
    Date
)

from .meta import Base


class Comment(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True)
    email = Column(Text())
    name = Column(Text())
    comment = Column(Text(), nullable=False)
    commented_date = Column(Date, nullable=False)
    marker_id = Column(Integer, nullable=False)
    user_id = Column(Integer)
