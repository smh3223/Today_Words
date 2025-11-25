from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api import routes
from .services.words import WordRepository

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_FILE = BASE_DIR / "data" / "words.json"

app = FastAPI(title="TodayWords", description="Korean vocabulary activation app")

# Allow local development across ports (frontend + backend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

repository = WordRepository(DATA_FILE)
app.include_router(routes.router)


@app.get("/", include_in_schema=False)
def root() -> dict:
    """Friendly root endpoint describing available routes."""
    return {
        "message": "TodayWords API",
        "routes": ["/health", "/words/today", "/progress/{user_id}", "/words/{word_id}/sentences"],
    }
