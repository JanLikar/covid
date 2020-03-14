from sqlalchemy import (
    func,
    Column,
    Integer,
    Text,
    UniqueConstraint,
)

from .meta import Base


class User(Base):
    __tablename__ = 'users'
    __table_args__ = (
        UniqueConstraint('passphrase', name='passphrase_uc'),
    )

    id = Column(Integer, primary_key=True)
    passphrase = Column(Text(), nullable=False)
    email = Column(Text())
