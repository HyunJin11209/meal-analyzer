# app.py
import streamlit as st

from database import NutritionDatabase
from evaluator import evaluate_from_foods
from nlp import FoodParser, build_food_vocab_from_db


st.set_page_config(page_title="Meal Analyzer", page_icon="🍱")

# DB 불러오기
db = NutritionDatabase(path="data/nutrition_db.json")

# NLP 준비하기
food_vocab = build_food_vocab_from_db(db)
parser = FoodParser(food_vocab)

st.title("🍱 Meal Analyzer")
st.write("먹은 메뉴를 입력하면 칼로리와 영양 정보를 보여주는 서비스입니다.")

user_text = st.text_area(
    "오늘 먹은 식단을 적어 주세요",
    placeholder="예: 아침에 토스트 2장, 우유 1컵 / 점심에 김치찌개, 공기밥 1그릇...",
)
# 성별 선택 UI
gender_kor = st.radio(
    "성별을 선택해 주세요.",
    options=["남성", "여성"],
    horizontal=True
)

# evaluator에서 쓰는 영어 코드로 변환
gender = "male" if gender_kor == "남성" else "female"


if st.button("분석하기"):
    if not user_text.strip():
        st.warning("식단 내용을 먼저 입력해 주세요! 😊")
    else:
        # NLP 수행
        food_counts = parser.extract_food_counts(user_text)
        food_list = list(food_counts.keys())

        if not food_list:
            st.error("❗️ 인식된 음식이 없습니다. 다시 입력해주세요!")
        else:
            st.write(f"🍽 감지된 음식: **{', '.join(food_list)}**")

            result = evaluate_from_foods(food_list, db, gender=gender)

            if "error" in result:
                st.error("DB에 음식 정보가 부족합니다.")
            else:
                st.subheader("📊 한 끼 섭취 칼로리 분석")
                st.metric("총 섭취 칼로리 (한끼)", f"{result['총 칼로리(kcal)']} kcal")

                st.subheader("🥗 영양소 비율 (%)")
                for k, v in result["영양 비율(%)"].items():
                    st.write(f"- **{k}**: {v}%")

                st.subheader("💡 건강 피드백")
                for f in result["영양 균형 피드백"]:
                    st.write(f"- {f}")

                st.subheader("🔥 칼로리 평가")
                st.success(result["칼로리 평가지"])
