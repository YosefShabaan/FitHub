from fastapi import FastAPI

from app.db.database import engine, Base
from app.models.user import User

Base.metadata.create_all(bind=engine)

app = FastAPI(title="FitHub API")

@app.get("/")
def root():
    return {
        "message": "FitHub API is running 🚀"
    }