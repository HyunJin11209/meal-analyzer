# 식사 영양 분석 + 건강 피드백 + 대체 식단 추천 로직

# ---- 기준 데이터 (건강 판단 기준 임시) ----
THRESHOLDS = {
    "calories": 700,   # 한 끼 기준 칼로리 상한 (예시)
    "protein": 25,     # 단백질 최소 권장량 (g)
    "fat": 30,         # 지방 상한 (g)
    "carbs": 90        # 탄수화물 상한 (g)
}


class MealEvaluator:
    """하나의 식사에 대한 영양 분석을 담당하는 클래스"""

    def __init__(self, thresholds=None):
        # 기준값을 바꾸고 싶으면 나중에 다른 dict를 넘겨줄 수 있음
        self.thresholds = thresholds or THRESHOLDS

    # ---- 1) 총 칼로리 계산 ----
    def calculate_calories(self, nutrition: dict) -> float:
        """
        nutrition 예시: {"protein": 20, "fat": 15, "carbs": 70}
        """
        protein = nutrition.get("protein", 0)
        fat = nutrition.get("fat", 0)
        carbs = nutrition.get("carbs", 0)

        calories = protein * 4 + carbs * 4 + fat * 9
        return round(calories, 1)

    # ---- 2) 건강 피드백 생성 ----
    def generate_health_feedback(self, calories: float, nutrition: dict) -> list:
        feedback = []

        # (1) 열량 평가
        if calories > self.thresholds["calories"]:
            feedback.append(" 섭취 열량이 권장량보다 높습니다. 다음 식사에서는 양을 줄여보세요.")
        elif calories < 400:
            feedback.append(" 비교적 가벼운 식사입니다. 영양소 균형이 맞는지 확인해보세요.")
        else:
            feedback.append(" 적절한 열량 섭취입니다.")

        # (2) 단백질 평가
        if nutrition.get("protein", 0) < self.thresholds["protein"]:
            feedback.append(" 단백질 섭취가 부족해요. 계란, 고기, 두부 등을 추가해보세요.")
        else:
            feedback.append(" 단백질 섭취가 충분합니다!")

        # (3) 지방 평가
        if nutrition.get("fat", 0) > self.thresholds["fat"]:
            feedback.append(" 지방 비율이 높습니다. 튀김류나 크림/버터 소스를 줄이는 것을 추천합니다.")

        return feedback

    # ---- 3) 대체 식단 추천 ----
    def recommend_alternative(self, nutrition: dict) -> list:
        recs = []

        if nutrition.get("protein", 0) < self.thresholds["protein"]:
            recs.append("추천: 닭가슴살 샐러드, 두부, 삶은 계란")
        if nutrition.get("fat", 0) > self.thresholds["fat"]:
            recs.append("추천: 튀김 대신 구이/찜, 에어프라이어 조리, 저지방 드레싱 사용")
        if nutrition.get("carbs", 0) > self.thresholds["carbs"]:
            recs.append("추천: 밥 양을 줄이고, 채소나 단백질 비중을 늘려보세요.")

        if not recs:
            recs.append(" 현재 식단은 매우 균형적이며 특별한 개선사항이 없습니다.")

        return recs

    # ---- 4) 전체 평가 함수 ----
    def evaluate(self, nutrition: dict) -> dict:
        """
        한 끼 식사에 대한 전체 평가 결과 반환
        """
        calories = self.calculate_calories(nutrition)
        feedback = self.generate_health_feedback(calories, nutrition)
        recommendation = self.recommend_alternative(nutrition)

        return {
            "calories": calories,
            "feedback": feedback,
            "recommendation": recommendation
        }


# ---- 테스트용 코드 ----
if __name__ == "__main__":
    sample = {"protein": 12, "fat": 35, "carbs": 80}
    evaluator = MealEvaluator()
    result = evaluator.evaluate(sample)
    print(result)

