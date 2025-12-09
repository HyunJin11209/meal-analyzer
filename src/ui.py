import streamlit as st

st.set_page_config(page_title="Meal Analyzer", page_icon="🍱")

st.title("🍱 Meal Analyzer")
st.write("먹은 메뉴를 입력하면 칼로리와 영양 정보를 보여주는 테스트 화면입니다.")

user_text = st.text_area(
    "오늘 먹은 식단을 적어 주세요",
    placeholder="예: 아침에 토스트 2장, 우유 1컵 / 점심에 김치찌개, 공기밥 1그릇...",
)

# 버튼을 한 번만 정의해서 변수에 저장
analyze_clicked = st.button("분석하기")

if analyze_clicked:
    if not user_text.strip():
        st.warning("식단 내용을 먼저 입력해 주세요!")
    else:
        # 테스트용 더미 데이터
        result = {
            "total_calories": 850,
            "nutrients": {
                "탄수화물": "적정 (50%)",
                "단백질": "조금 부족 (15%)",
                "지방": "약간 높음 (35%)",
                "나트륨": "권장량보다 높음",
            },
            "feedback": [
                "오늘 지방과 나트륨 섭취가 조금 많은 편입니다.",
                "단백질이 부족하니 다음 끼니에 계란, 콩, 닭가슴살 등을 추가하면 좋아요.",
            ],
            "alternatives": [
                "치킨버거 대신 그릴드 치킨 샐러드는 어떨까요?",
                "탄산음료 대신 물 또는 무가당 티를 추천드립니다.",
            ],
        }

        st.subheader("📊 예상 칼로리")
        st.metric("총 섭취 칼로리", f"{result['total_calories']} kcal")

        st.subheader("🥗 영양소 분석")
        for k, v in result["nutrients"].items():
            st.write(f"- **{k}**: {v}")

        st.subheader("💡 건강 피드백")
        for f in result["feedback"]:
            st.write(f"- {f}")

        st.subheader("🍽 대체 식단 추천")
        for a in result["alternatives"]:
            st.write(f"- {a}")
