from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from app.api.routes import auth, dashboard, members, portal, subscriptions
from app.db.database import Base, engine
from app.db.schema import ensure_runtime_schema
from app.models.member import Member
from app.models.subscription import Subscription
from app.models.user import User
from app.services.admin_seed import seed_default_admin

Base.metadata.create_all(bind=engine)
ensure_runtime_schema(engine)
seed_default_admin()

app = FastAPI(title="FitHub API")

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(members.router, prefix="/members", tags=["Members"])
app.include_router(subscriptions.router, prefix="/subscriptions", tags=["Subscriptions"])
app.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])
app.include_router(portal.router, prefix="/portal", tags=["Portal"])

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
