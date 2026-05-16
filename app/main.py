from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from app.api.routes import auth, dashboard, members, subscriptions
from app.db.database import Base, engine
from app.models.member import Member
from app.models.subscription import Subscription
from app.models.user import User

Base.metadata.create_all(bind=engine)

app = FastAPI(title="FitHub API")

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(members.router, prefix="/members", tags=["Members"])
app.include_router(subscriptions.router, prefix="/subscriptions", tags=["Subscriptions"])
app.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])

frontend_dir = Path(__file__).resolve().parent / "frontend"
if frontend_dir.exists():
    app.mount("/frontend", StaticFiles(directory=frontend_dir, html=True), name="frontend")


@app.get("/")
def root():
    if frontend_dir.exists():
        return RedirectResponse(url="/frontend/pages/index.html")
    return {"message": "FitHub API is running"}


@app.get("/health")
def health():
    return {"status": "ok"}
