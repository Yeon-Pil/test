# Hackathon AI Demo

FastAPI 백엔드가 AI를 호출하고, Streamlit 화면이 백엔드 API를 사용하는 최소 예제입니다.

## 1. 가상환경 생성

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Windows CMD:

```bat
python -m venv .venv
.venv\Scripts\activate
```

## 2. 패키지 설치

```bash
pip install -r requirements.txt
```

## 3. 환경변수 파일 만들기

Windows:

```bat
copy .env.example .env
```

macOS/Linux:

```bash
cp .env.example .env
```

`.env`의 `OPENAI_API_KEY`를 비워두면 mock 결과가 반환됩니다.
실제 AI 호출을 하려면 API 키를 입력하세요.

## 4. 백엔드 실행

프로젝트 최상위 폴더에서:

```bash
uvicorn backend.main:app --reload --port 8000
```

확인 주소:

- API 기본 주소: http://127.0.0.1:8000
- API 문서: http://127.0.0.1:8000/docs
- 상태 확인: http://127.0.0.1:8000/health

## 5. 프론트엔드 실행

새 터미널을 열고 가상환경을 다시 활성화한 뒤:

```bash
streamlit run frontend/app.py
```

## 6. 코드 흐름

1. 사용자가 Streamlit 화면에 텍스트를 입력합니다.
2. `requests.post()`가 FastAPI의 `/analyze`로 JSON을 전송합니다.
3. FastAPI가 Pydantic으로 입력을 검사합니다.
4. `run_ai()`가 OpenAI API 또는 mock 함수를 실행합니다.
5. 결과가 JSON으로 프론트엔드에 반환됩니다.
6. Streamlit이 결과를 화면에 표시합니다.

## 7. 직접 연습할 부분

- `AnalyzeRequest`에 `age`, `monthly_income` 필드를 추가하기
- 출력에 `score: int` 추가하기
- 프롬프트를 금융, ESG, 보이스피싱 등 해커톤 주제로 변경하기
- 잘못된 입력을 넣어 422 오류 확인하기
- 백엔드 서버를 끄고 프론트의 연결 오류 확인하기
