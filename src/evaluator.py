# 식사 영양 분석 + 건강 피드백 + 대체 식단 추천 로직
"""
Evaluator Module

- DB/NLP가 제공한 food_list와 nutrition 데이터 기반으로
  건강 분석, 칼로리 계산, 식단 피드백을 제공하는 수정.

- 평가 기준:
  · 19~29세 성인 기준
  · 성별별 권장 칼로리
     - 남성: 2600kcal/day
     - 여성: 2000kcal/day
  · 에너지 비율 기준 (탄수화물/단백질/지방):
     - 탄수화물: 55~65%
     - 단백질: 7~20%
     - 지방: 15~30%
"""

# ------------------------- 기준값 설정 -------------------------

NUTRITION_STANDARD = {
    "daily_calories": {
        "male": 2600,
        "female": 2000
    },
    "ratio": {
        "carbs": (55, 65),
        "protein": (7, 20),
        "fat": (15, 30)
    }
}


# ------------------------- 계산 함수 -------------------------

def calculate_calories(nutrition):
    """탄4 + 단4 + 지방9 규칙."""
    return (nutrition["protein"] * 4) + (nutrition["carbs"] * 4) + (nutrition["fat"] * 9)


def calculate_ratio(nutrition):
    """에너지 비율 (%) 계산"""
    total_cal = calculate_calories(nutrition)

    if total_cal == 0:
        return {"carbs": 0, "protein": 0, "fat": 0}

    return {
        "carbs": round((nutrition["carbs"] * 4 / total_cal) * 100, 1),
        "protein": round((nutrition["protein"] * 4 / total_cal) * 100, 1),
        "fat": round((nutrition["fat"] * 9 / total_cal) * 100, 1)
    }


# ------------------------- 평가 로직 -------------------------

def analyze_ratio_balance(ratio):
    """탄/단/지 비율 기반 피드백 생성"""
    fb = []

    carb_range = NUTRITION_STANDARD["ratio"]["carbs"]
    protein_range = NUTRITION_STANDARD["ratio"]["protein"]
    fat_range = NUTRITION_STANDARD["ratio"]["fat"]

    # 탄수화물
    if ratio["carbs"] < carb_range[0]:
        fb.append(" 탄수화물 섭취가 부족합니다. 밥이나 고구마, 잡곡, 국수 등을 추가하세요.")
    elif ratio["carbs"] > carb_range[1]:
        fb.append(" 탄수화물 비율이 높습니다. 밥이나 빵 양을 조금 줄여보세요.")

    # 단백질
    if ratio["protein"] < protein_range[0]:
        fb.append(" 단백질 섭취가 부족합니다. 계란, 닭가슴살, 콩류, 돼지고기/소고기를 추가해보세요.")
    elif ratio["protein"] > protein_range[1]:
        fb.append(" 단백질 비율이 높습니다. 전체 식사 균형을 점검해보세요.")

    # 지방
    if ratio["fat"] < fat_range[0]:
        fb.append(" 지방 섭취가 부족합니다. 견과류·참기름·연어·아보카도 같은 건강한 지방을 조금 추가해보세요.")
    elif ratio["fat"] > fat_range[1]:
        fb.append(" 지방 섭취가 높습니다. 기름에 볶은 음식이나 비빔소스, 국물 섭취량 및 튀김 등을 줄여보세요.")

    return fb


def calorie_feedback(total_calories, gender="female"):
    """한 끼 적정 칼로리 기준"""
    meal_limit = NUTRITION_STANDARD["daily_calories"][gender] / 3

    if total_calories < meal_limit * 0.7:
        return " 비교적 가벼운 식사입니다."
    elif total_calories > meal_limit * 1.2:
        return f" 칼로리 과다! (추천 기준: {meal_limit:.0f} kcal)"
    return " 칼로리가 적정 범위입니다."


# ------------------------- 여러 음식 합산 -------------------------

def combine_nutrition(nutrition_list):
    """DB에서 가져온 음식 여러 개의 영양값 합산"""
    total = {"protein": 0, "fat": 0, "carbs": 0}
    for n in nutrition_list:
        total["protein"] += n.get("protein", 0)
        total["fat"] += n.get("fat", 0)
        total["carbs"] += n.get("carbs", 0)
    return total


# ------------------------- 최종 평가 함수 -------------------------

def evaluate_from_foods(food_list, db, gender="female"):
    """NLP food list → DB nutrition → 평가"""
    nutrition_data = []

    for food in food_list:
        value = db.get_nutrition(food)
        if value:
            nutrition_data.append(value)

    if not nutrition_data:
        return {"error": "❗ DB에 음식 데이터가 없습니다."}

    total = combine_nutrition(nutrition_data)
    total_cal = calculate_calories(total)
    ratio = calculate_ratio(total)

    return {
        "감지된 음식": food_list,
        "총 칼로리(kcal)": total_cal,
        "영양 비율(%)": ratio,
        "칼로리 평가지": calorie_feedback(total_cal, gender),
        "영양 균형 피드백": analyze_ratio_balance(ratio)
    }
 

