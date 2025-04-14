from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(String, unique=True, index=True)
    username = Column(String)
    is_premium = Column(Integer, default=0)

    actions = relationship("Action", back_populates="user")

class Movie(Base):
    __tablename__ = "movies"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)
    trailer_url = Column(String)
    tags = Column(String)  # жанры и ключевые слова
    image_url = Column(String)

    actions = relationship("Action", back_populates="movie")

class Action(Base):
    __tablename__ = "actions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    movie_id = Column(Integer, ForeignKey("movies.id"))
    action_type = Column(String)  # like / save / comment
    comment = Column(Text, nullable=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="actions")
    movie = relationship("Movie", back_populates="actions")
