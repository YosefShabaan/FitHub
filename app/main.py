from fastapi import FastAPI
from app.db.database import engine, Base
from app.models.user import User
from app.models.member import Member
from app.models.subscription import Subscription
from app.api.routes import auth, members, subscriptions, dashboard

Base.metadata.create_all(bind=engine)

app = FastAPI(title="FitHub API")

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(members.router, prefix="/members", tags=["Members"])
app.include_router(subscriptions.router, prefix="/subscriptions", tags=["Subscriptions"])
app.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])

@app.get("/")
def root():
    return {"message": "FitHub API is running 🚀"}
