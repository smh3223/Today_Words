from typing import List

from pydantic import BaseModel


class Word(BaseModel):
    id: int
    word: str
    meaning: str
    nuance: str
    examples: List[str]
    similar_words: List[str]
