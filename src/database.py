import json
import os

DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "nutrition_db.json")


class NutritionDatabase:
    def __init__(self):
        self.data = self.load()
        self.db = self.data  # ⚡ NLP 코드 호환용

    def load(self):
        """nutrition_db.json 불러오기"""
        if not os.path.exists(DATA_PATH):
            return {}
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            return json.load(f)

    def get(self, food_name):
        """음식 영양정보 반환"""
        return self.data.get(food_name)

    def get_nutrition(self, food_name):
        """⚡ evaluator.py에서 호출하는 메서드"""
        return self.data.get(food_name)

    def search(self, keyword):
        """키워드 포함하는 음식 리스트 반환"""
        return {k: v for k, v in self.data.items() if keyword in k}

    def add(self, food_name, values):
        """새 음식 추가"""
        self.data[food_name] = values
        self.db = self.data
        self.save()

    def save(self):
        """nutrition_db.json 저장"""
        with open(DATA_PATH, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
