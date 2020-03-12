from sqlalchemy import (
    func,
    Column,
    Integer,
    Text,
)

from .meta import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    passphrase = Column(Text(), nullable=False)
