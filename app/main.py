from fastapi import FastAPI

app = FastAPI(title="FitHub API")

@app.get("/")
def root():
    return {
        "message": "FitHub API is running 🚀"
    }