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
    # 공백 체크
    if not user_text.strip():
        st.warning("식단 내용을 먼저 입력해 주세요! 😊")
    else:
        # NLP 수행: 문장에서 음식 추출
        food_counts = parser.extract_food_counts(user_text)
        food_list = list(food_counts.keys())

        # 1차: 아무 음식도 못 찾았을 때
        if not food_list:
            st.error("⚠ 인식된 음식이 없습니다. 다시 입력해주세요!")
        else:
            # DB 여부 체크
            found_foods = [food for food in food_list if db.get_nutrition(food)]
            missing_foods = [food for food in food_list if not db.get_nutrition(food)]

            # 감지된 음식 먼저 보여주기
            st.write(f"🍽 감지된 음식: **{', '.join(food_list)}**")

            # DB에 없는 음식 알려주기
            if missing_foods:
                st.warning(f"❗ DB에 없는 음식: {', '.join(missing_foods)}")

            # DB에 있는 음식이 하나도 없으면 분석 불가
            if not found_foods:
                st.error("❌ 분석 가능한 음식이 없습니다. (DB에 등록된 식품이 없음)")
                st.info("👉 메뉴를 더 자세히 입력하거나 다른 음식을 입력해보세요.")
            else:
                # 정상 분석
                result = evaluate_from_foods(found_foods, db, gender=gender)

                # 분석 완료 표시
                st.success("🍀 분석 완료!")

                # 디버깅용 원본 JSON도 보고 싶으면
                st.json(result)

                # 👇 보기 좋게 정리해서도 보여주기 (한 끼 기준)
                if "error" in result:
                    st.error("DB에 음식 정보가 부족합니다.")
                else:
                    st.subheader("📊 한 끼 섭취 칼로리 분석")
                    st.metric("총 섭취 칼로리 (한 끼)", f"{result['총 칼로리(kcal)']} kcal")

                    st.subheader("🥗 영양소 비율 (%)")
                    for k, v in result["영양 비율(%)"].items():
                        st.write(f"- **{k}**: {v}%")

                    st.subheader("💡 건강 피드백")
                    for f in result["영양 균형 피드백"]:
                        st.write(f"- {f}")

                    st.subheader("🔥 칼로리 평가")
                    st.success(result["칼로리 평가지"])
