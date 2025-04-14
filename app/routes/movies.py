from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.recommender import get_movie_recommendations
from app.models import Movie

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/movies")
def get_movies(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(Movie).offset(skip).limit(limit).all()

@router.get("/recommendations")
def recommendations(user_id: int = Query(...), db: Session = Depends(get_db)):
    return get_movie_recommendations(user_id=user_id, db=db)
