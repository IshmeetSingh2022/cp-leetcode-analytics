from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.database import Base, engine
from app.middleware.auth import auth_middleware
from app.middleware.logging import logging_middleware
from app.api.profile import router as profile_router
import app.models

from app.api import auth, routes_user, recommendation, stats, topic_tracker

app = FastAPI(
    title="CP Analytics AI",
    description="AI-powered Competitive Programming Analytics Platform",
    version="1.0.0",
)

# --- Middleware ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(BaseHTTPMiddleware, dispatch=logging_middleware)
app.add_middleware(BaseHTTPMiddleware, dispatch=auth_middleware)

# --- Database ---
@app.on_event("startup")
def create_tables():
    Base.metadata.create_all(bind=engine)

# --- Health check ---
@app.get("/", tags=["Health"])
def root():
    return {"message": "CP Analytics AI backend running 🚀"}

# --- Routers ---
app.include_router(auth.router)
app.include_router(routes_user.router)
app.include_router(recommendation.router)
app.include_router(stats.router)
app.include_router(profile_router)
app.include_router(topic_tracker.router)