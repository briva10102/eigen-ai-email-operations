from fastapi import FastAPI
from backend.app.core.config import settings
from backend.app.api.reviews import router as reviews_router
import backend.app.db.models
from backend.app.api.processing import router as processing_router

app = FastAPI(title=settings.app_name)
app.include_router(reviews_router)
app.include_router(processing_router)


@app.get("/")
def root():
    return {"message": "EIGEN AI Email Operations is running"}