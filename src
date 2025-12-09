import json
import os

class NutritionDatabase:
    def __init__(self, path="data/nutrition_db.json"):
        self.db_path = path
        self.db = self._load_database()

    def _load_database(self):
        if not os.path.exists(self.db_path):
            raise FileNotFoundError(f"Nutrition DB not found: {self.db_path}")
        
        with open(self.db_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def get_nutrition(self, food_name):
        """음식 이름으로 영양 정보를 가져오는 함수"""
        return self.db.get(food_name, None)

    def search_food(self, keyword):
        """키워드로 음식 부분 검색"""
        return [name for name in self.db.keys() if keyword in name]
