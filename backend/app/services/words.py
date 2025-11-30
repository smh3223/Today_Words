import json
from datetime import date
from pathlib import Path
from typing import Dict, List, Optional

from ..models.word import Word


class WordRepository:
    """Simple in-memory repository backed by a JSON seed file."""

    def __init__(self, data_file: Path) -> None:
        self.data_file = data_file
        self._words: List[Word] = []
        self._progress: Dict[str, Dict[str, object]] = {}
        self._load_words()

    def _load_words(self) -> None:
        if not self.data_file.exists():
            raise FileNotFoundError(f"Word data file not found: {self.data_file}")

        raw = json.loads(self.data_file.read_text(encoding="utf-8"))
        self._words = [Word(**item) for item in raw]

    @property
    def words(self) -> List[Word]:
        return self._words

    def get_today_word(self, target_date: Optional[date] = None) -> Word:
        if not self._words:
            raise ValueError("Word list is empty")

        active_date = target_date or date.today()
        index = active_date.toordinal() % len(self._words)
        return self._words[index]

    def track_seen(self, user_id: str, word_id: int) -> None:
        progress = self._progress.setdefault(user_id, {"seen": set(), "written": {}})
        progress["seen"].add(word_id)

    def record_sentence(self, user_id: str, word_id: int, sentence: str) -> None:
        progress = self._progress.setdefault(user_id, {"seen": set(), "written": {}})
        progress["seen"].add(word_id)
        written = progress["written"].setdefault(word_id, [])
        written.append(sentence)

    def get_progress(self, user_id: str) -> Dict[str, object]:
        progress = self._progress.get(user_id, {"seen": set(), "written": {}})
        # Convert sets for JSON friendliness
        return {
            "seen": sorted(progress.get("seen", set())),
            "written": progress.get("written", {}),
        }
