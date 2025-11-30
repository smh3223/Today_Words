# TodayWords

TodayWords는 익숙한 한국어 어휘를 적극적으로 쓰도록 돕는 웹앱입니다. 하루에 한 단어씩 예문과 비슷한 표현을 확인하고, 직접 문장을 작성해 단어를 활성화하는 것을 목표로 합니다.

## 프로젝트 구조 제안

- `backend/`
  - `app/main.py`: FastAPI 애플리케이션 엔트리포인트
  - `app/api/routes.py`: 주요 API 라우트 정의 (헬스체크, 오늘의 단어, 진행도, 문장 제출)
  - `app/services/words.py`: 단어 데이터 로딩 및 간단한 진행도 관리
  - `app/models/word.py`: Pydantic 모델 정의
  - `tests/`: Pytest 예제 테스트
  - `requirements.txt`: 백엔드 의존성 목록
- `data/words.json`: 초기 단어 시드 데이터
- `frontend/index.html`: 단순 HTML/JS로 오늘의 단어를 보여주는 페이지

## 백엔드 실행 방법

1. 의존성 설치:

   ```bash
   cd backend
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. 개발 서버 실행:

   프로젝트 루트가 아닌 `backend` 디렉터리를 기준으로 실행해야 `app` 모듈을 찾을 수 있습니다. 루트에서 바로 실행하려면 `--app-dir backend` 옵션을 사용하세요.

   ```bash
   # (추천) backend 디렉터리에서 실행
   cd backend
   uvicorn app.main:app --reload --port 8000

   # 또는 루트에서 실행
   cd ..  # 루트에 있는 경우 생략
   uvicorn app.main:app --reload --port 8000 --app-dir backend
   ```

3. 테스트 실행:

   ```bash
   pytest
   ```

## 프런트엔드 실행 방법

프런트엔드는 정적 HTML/JS로 구성되어 있어 별도 빌드 과정이 없습니다. 다음과 같이 간단한 개발 서버로 실행할 수 있습니다.

```bash
python -m http.server 3000 -d frontend
```

서버가 실행되면 브라우저에서 `http://localhost:3000`으로 접속하세요. 백엔드가 `localhost:8000`에서 실행 중이어야 데이터를 받아올 수 있습니다.

## 단어 데이터 추가 방법

- `data/words.json` 파일에 항목을 추가합니다. 각 항목은 아래 형식을 따릅니다.

```json
{
  "id": 4,
  "word": "단어",
  "meaning": "의미 설명",
  "nuance": "뉘앙스나 쓰임새",
  "examples": ["예문 1", "예문 2"],
  "similar_words": ["관련 표현 1", "관련 표현 2"]
}
```

- `id`는 고유해야 하며, `examples`와 `similar_words`는 문자열 배열로 제공합니다.
