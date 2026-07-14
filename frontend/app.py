import os

import requests
import streamlit as st

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

st.set_page_config(
    page_title="AI 행동 코치",
    page_icon="🤖",
    layout="centered",
)

st.title("🤖 AI 행동 코치")
st.caption("사용자의 고민을 입력하면 AI가 핵심 문제와 다음 행동을 정리합니다.")

user_text = st.text_area(
    "상황을 입력하세요",
    placeholder="예: 월급을 받으면 계획 없이 소비해서 저축을 거의 못 하고 있어요.",
    height=160,
)

if st.button("AI 분석", type="primary", use_container_width=True):
    if len(user_text.strip()) < 5:
        st.warning("상황을 5자 이상 입력해주세요.")
    else:
        try:
            with st.spinner("분석 중입니다..."):
                response = requests.post(
                    f"{API_URL}/analyze",
                    json={"text": user_text},
                    timeout=90,
                )
                response.raise_for_status()
                result = response.json()

            st.success("분석이 완료되었습니다.")

            st.subheader("요약")
            st.write(result["summary"])

            risk_labels = {
                "low": "낮음",
                "medium": "보통",
                "high": "높음",
            }
            st.metric("위험 수준", risk_labels[result["risk_level"]])

            st.subheader("핵심 발견")
            for item in result["key_findings"]:
                st.write(f"- {item}")

            st.subheader("추천 행동")
            for index, item in enumerate(result["recommendations"], start=1):
                st.write(f"{index}. {item}")

            st.subheader("지금 할 일")
            st.info(result["next_action"])

        except requests.exceptions.ConnectionError:
            st.error(
                "백엔드 서버에 연결할 수 없습니다. "
                "먼저 uvicorn 서버가 실행 중인지 확인하세요."
            )
        except requests.exceptions.Timeout:
            st.error("AI 응답 시간이 초과되었습니다.")
        except requests.exceptions.HTTPError:
            try:
                detail = response.json().get("detail", "서버 오류")
            except ValueError:
                detail = "서버 오류"
            st.error(f"요청 실패: {detail}")
