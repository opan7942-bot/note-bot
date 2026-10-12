import os
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
from backend.bot_database import init_db
from backend.routes import router

load_dotenv()

app = FastAPI()

app.include_router(router)
app.mount(
    "/mini-app",
    StaticFiles(directory=Path(__file__).resolve().parent.parent / "mini-app", html=True),
    name="mini-app",
)


@app.on_event("startup")
def initialize_database():
    if not os.getenv("TELEGRAM_TOKEN"):
        raise RuntimeError("TELEGRAM_TOKEN must be set in the project .env file")
    if not os.getenv("API_SECRET_KEY"):
        raise RuntimeError("API_SECRET_KEY must be set in the project .env file")
    init_db()
