from sqlalchemy import Column, Integer, String
from leads_package.databases import Base
from enum import Enum


class ReachedOutState(Enum):
    PENDING = 0
    REACHED_OUT = 1


class User(Base):
    __tablename__ = 'users2'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    firstname = Column(String(50), nullable=False)
    lastname = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    state = Column(String(50), default=ReachedOutState.PENDING.name, nullable=False)
    resume = Column(String(500), nullable=False)
