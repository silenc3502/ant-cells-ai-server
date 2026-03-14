from datetime import datetime

from sqlalchemy import Column, DateTime, String, Text
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class PostORM(Base):
    __tablename__ = "posts"

    id = Column(String(36), primary_key=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    author = Column(String(100), nullable=False, default="anonymous")
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
