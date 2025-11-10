from typing import Dict
from fastapi import FastAPI
from .api.v1.api_router import api_v1_router
from .core.config import settings
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    description="API Gateway for Mikroserwisu Kursów",
)

# Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_v1_router)

@app.get("/", tags=["Root"])
def health_check() -> dict[str, str]:
    return {
        "message": "Welcome to API Gateway",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "running",
    }