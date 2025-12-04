# ---- 기준 데이터 (건강 판단 기준 임시) ----
THRESHOLDS = {
    "calories": 700,
    "protein": 25,
    "fat": 30,
    "carbs": 90
}


# ---- 1) 총 칼로리 계산 ----
def calculate_total_calories(nutrition):
    protein = nutrition.get("protein", 0)
    fat = nutrition.get("fat", 0)
    carbs = nutrition.get("carbs", 0)

    calories = protein * 4 + carbs * 4 + fat * 9
    return round(calories, 1)


# ---- 2) 건강 피드백 생성 ----
def generate_health_feedback(calories, nutrition):
    feedback = []

    if calories > THRESHOLDS["calories"]:
        feedback.append(" 섭취 열량이 권장량보다 높습니다. 다음 식사에서는 양을 줄여보세요.")
    elif calories < 400:
        feedback.append(" 비교적 가벼운 식사입니다. 영양소 균형이 맞는지 확인해보세요.")
    else:
        feedback.append(" 적절한 열량 섭취입니다.")

    if nutrition["protein"] < THRESHOLDS["protein"]:
        feedback.append(" 단백질 섭취가 부족해요. 계란, 고기, 두부 등을 추가해보세요.")
    else:
        feedback.append(" 단백질 섭취가 충분합니다!")

    if nutrition["fat"] > THRESHOLDS["fat"]:
        feedback.append(" 지방 비율이 높습니다. 튀김류나 소스 섭취 등을 줄이는 것을 추천합니다.")

    return feedback


# ---- 3) 대체 식단 추천 ----
def recommend_alternative(nutrition):
    recs = []

    if nutrition["protein"] < THRESHOLDS["protein"]:
        recs.append("추천: 닭가슴살 샐러드, 두부, 삶은 계란")
    if nutrition["fat"] > THRESHOLDS["fat"]:
        recs.append("추천: 에어프라이어 조리, 저지방 드레싱")
    if nutrition["carbs"] > THRESHOLDS["carbs"]:
        recs.append("추천: 밥 양 줄이고, 채소 섭취 늘리기")

    if not recs:
        recs.append("✨ 현재 식단은 매우 균형적이며 추천 개선사항이 없습니다!")

    return recs


# ---- 최종 실행 결과 패키징 ----
def evaluate_meal(nutrition):
    calories = calculate_total_calories(nutrition)
    feedback = generate_health_feedback(calories, nutrition)
    recommendation = recommend_alternative(nutrition)

    return {
        "calories": calories,
        "feedback": feedback,
        "recommendation": recommendation
    }


# ---- 테스트 코드 ----
if __name__ == "__main__":
    sample = {"protein": 12, "fat": 35, "carbs": 80}
    print(evaluate_meal(sample))
