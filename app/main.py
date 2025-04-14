from fastapi import FastAPI
from app.routes import users, movies, actions
from app.database import engine, Base

app = FastAPI()
Base.metadata.create_all(bind=engine)

app.include_router(users.router)
app.include_router(movies.router)
app.include_router(actions.router)

@app.get("/")
def read_root():
    return {"msg": "Movie recommendation API is live"}
