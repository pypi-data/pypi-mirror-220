# main.py
from fastapi import FastAPI
from .models import models_router
from .generate import generate_router

app = FastAPI()

app.include_router(models_router, prefix="/models", tags=["Models"])
app.include_router(generate_router, prefix="/generate", tags=["Generate"])