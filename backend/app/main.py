from fastapi import FastAPI
from backend.app.core.config import settings

app = FastAPI(title=settings.app_name)


@app.get("/")
def root():
    return {"message": "EIGEN AI Email Operations is running"}