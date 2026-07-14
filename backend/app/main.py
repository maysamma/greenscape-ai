from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.database.base import Base
from app.database.database import engine

import app.models


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="GreenScape AI",
    version="1.0.0",
    description=(
        "Autonomous Multi-Agent AI Platform "
        "for Sustainable Architectural Design Review"
    ),
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)


@app.get("/")
async def root():
    return {
        "message": "GreenScape AI API is running",
    }


@app.get("/health")
async def health():
    return {
        "status": "healthy",
    }