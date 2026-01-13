from sqlalchemy import Column, Integer, String, Text
from .database import Base

class Film(Base):
    __tablename__ = "films"

    show_id = Column(String(50), primary_key=True, index=True)
    type = Column(String(50))
    title = Column(String(255))
    director = Column(Text)
    cast = Column(Text)
    country = Column(Text)
    date_added = Column(String(100))
    release_year = Column(Integer)
    rating = Column(String(50))
    duration = Column(String(50))
    listed_in = Column(Text)
    description = Column(Text)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    hashed_password = Column(String(100))