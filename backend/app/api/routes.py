from fastapi import APIRouter, Depends, HTTPException

from ..models.word import Word
from ..services.words import WordRepository

router = APIRouter()


def get_repository() -> WordRepository:
    from ..main import repository

    return repository


@router.get("/health", summary="Basic health check")
def health_check() -> dict:
    return {"status": "ok"}


@router.get("/words/today", response_model=Word, summary="Get today's word")
def read_today_word(user_id: str = "guest", repo: WordRepository = Depends(get_repository)) -> Word:
    word = repo.get_today_word()
    repo.track_seen(user_id, word.id)
    return word


@router.post(
    "/words/{word_id}/sentences",
    status_code=201,
    summary="Store a sentence written by the user",
)
def submit_sentence(
    word_id: int,
    payload: dict,
    user_id: str = "guest",
    repo: WordRepository = Depends(get_repository),
) -> dict:
    sentence = payload.get("sentence")
    if not sentence:
        raise HTTPException(status_code=400, detail="Sentence text is required")

    repo.record_sentence(user_id, word_id, sentence)
    return {"word_id": word_id, "sentence": sentence}


@router.get("/progress/{user_id}", summary="Retrieve simple progress for a user")
def read_progress(user_id: str, repo: WordRepository = Depends(get_repository)) -> dict:
    return repo.get_progress(user_id)
