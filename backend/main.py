import os
from enum import Enum

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from openai import OpenAI
from pydantic import BaseModel, Field

load_dotenv()

app = FastAPI(
    title="Hackathon AI Demo API",
    description="사용자 고민을 분석해 구조화된 결과를 반환하는 예제",
    version="1.0.0",
)


class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class AnalyzeRequest(BaseModel):
    text: str = Field(
        min_length=5,
        max_length=2000,
        description="AI가 분석할 사용자의 상황",
    )


class AnalyzeResult(BaseModel):
    summary: str
    risk_level: RiskLevel
    key_findings: list[str]
    recommendations: list[str]
    next_action: str


def make_mock_result(text: str) -> AnalyzeResult:
    """API 키가 없을 때도 화면 연결을 연습할 수 있는 가짜 결과."""
    return AnalyzeResult(
        summary=f"입력 내용을 바탕으로 핵심 문제를 분석했습니다: {text[:40]}",
        risk_level=RiskLevel.MEDIUM,
        key_findings=[
            "현재 상황에 대한 정보가 일부 부족합니다.",
            "우선순위를 정하면 실행 가능성이 높아집니다.",
        ],
        recommendations=[
            "가장 중요한 목표 한 가지를 먼저 정하세요.",
            "목표를 이번 주에 할 수 있는 작은 행동으로 나누세요.",
        ],
        next_action="오늘 실행할 행동 한 가지를 선택하세요.",
    )


def run_ai(text: str) -> AnalyzeResult:
    api_key = os.getenv("OPENAI_API_KEY")

    # 키가 없으면 mock 모드로 동작한다.
    if not api_key:
        return make_mock_result(text)

    client = OpenAI(api_key=api_key)

    response = client.responses.parse(
        model=os.getenv("OPENAI_MODEL", "gpt-5.6-luna"),
        input=[
            {
                "role": "system",
                "content": (
                    "당신은 사용자의 문제를 분석하는 한국어 AI 코치입니다. "
                    "과장하지 말고, 입력에 근거해 핵심 문제와 실행 가능한 조언을 제시하세요. "
                    "risk_level은 low, medium, high 중 하나로 판단하세요."
                ),
            },
            {
                "role": "user",
                "content": text,
            },
        ],
        text_format=AnalyzeResult,
    )

    if response.output_parsed is None:
        raise RuntimeError("AI 응답을 구조화된 결과로 변환하지 못했습니다.")

    return response.output_parsed


@app.get("/")
def root():
    return {"message": "Hackathon AI Demo API"}


@app.get("/health")
def health():
    return {
        "status": "ok",
        "mode": "openai" if os.getenv("OPENAI_API_KEY") else "mock",
    }


@app.post("/analyze", response_model=AnalyzeResult)
def analyze(request: AnalyzeRequest):
    try:
        return run_ai(request.text)
    except Exception as exc:
        # 실제 서비스에서는 상세 오류를 로그에만 남기는 편이 안전하다.
        raise HTTPException(
            status_code=500,
            detail="AI 분석 중 오류가 발생했습니다.",
        ) from exc
