from sqlalchemy import Column, Integer, String, Text, UniqueConstraint, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Article(Base):
    __tablename__ = 'articles'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    content = Column(Text)
    date = Column(DateTime(timezone=True)) 
    url = Column(String, unique=True)
    author = Column(String, nullable=True, default="Unknown")
    summary = Column(String, nullable=True, default="Unknown")
    topic = Column(String, nullable=True, default="Unknown")
