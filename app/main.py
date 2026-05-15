from fastapi import FastAPI

from app.db.database import engine, Base

from app.models.user import User

from app.api.routes import auth

Base.metadata.create_all(bind=engine)

app = FastAPI(title="FitHub API")

app.include_router(
    auth.router,
    prefix="/auth",
    tags=["Authentication"]
)

@app.get("/")
def root():
    return {
        "message": "FitHub API is running 🚀"
    }