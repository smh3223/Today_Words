from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_today_word_structure():
    response = client.get("/words/today")
    assert response.status_code == 200
    body = response.json()
    for field in ["id", "word", "meaning", "nuance", "examples", "similar_words"]:
        assert field in body
