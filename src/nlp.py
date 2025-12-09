# src/nlp.py

from typing import Dict, List
import re
from transformers import AutoTokenizer
from database import NutritionDatabase

print("DEBUG: 코드 실행됨")


def _normalize(text: str) -> str:
    """공백 제거 + 소문자로 통일."""
    return text.replace(" ", "").lower()


def build_food_vocab_from_db(db: NutritionDatabase) -> Dict[str, List[str]]:
    """NutritionDatabase에 있는 음식 이름으로 vocab 생성."""
    vocab: Dict[str, List[str]] = {}

    for name in db.db.keys():
        vocab[name] = [name]

    extra_synonyms: Dict[str, List[str]] = {
        # 필요하면 여기서만 팀원들과 합의해서 동의어 추가
    }

    for canonical, syns in extra_synonyms.items():
        if canonical in vocab:
            vocab[canonical] = list(set(vocab[canonical] + syns))

    return vocab


class FoodParser:
    def __init__(self, food_vocab: Dict[str, List[str]]):
        """
        food_vocab: {대표 음식 이름: [동의어1, 동의어2, ...]}
        """
        self.food_vocab = food_vocab
        self.tokenizer = AutoTokenizer.from_pretrained("klue/bert-base")

    def extract_food_names(self, text: str) -> list[str]:
        """
        1) vocab에 있는 음식/동의어가 문장에 등장하면 매칭
        2) '김치볶음밥'과 '볶음밥'처럼 포함 관계일 때는
           더 긴 이름만 남기고 짧은 이름은 제거
        """
        print(f"[DEBUG] extract_food_names 호출: {text}")

        text_clean = text.strip()
        matched: list[str] = []

        for canonical, synonyms in self.food_vocab.items():
            candidates = set(synonyms) | {canonical}

            for cand in candidates:
                if cand and cand in text_clean:
                    matched.append(canonical)
                    break

        if not matched:
            return []

        unique_matched: list[str] = []
        for food in matched:
            if food not in unique_matched:
                unique_matched.append(food)

        result: list[str] = []
        for food in sorted(unique_matched, key=len, reverse=True):
            if any(food in longer for longer in result):
                continue
            result.append(food)

        return result

    def extract_food_counts(self, text: str) -> dict[str, int]:
        """
        문장에서 '음식 이름 + 개수'를 찾아
        {대표 음식 이름: 개수} 형태로 반환.
        """
        print(f"[DEBUG] extract_food_counts 호출: {text}")
        text_clean = text.strip()
        counts: dict[str, int] = {}

        units = r"(개|그릇|접시|마리|판|줄|조각|공기|컵|인분)?"

        kor_num_map = {
            "한": 1,
            "두": 2,
            "세": 3,
            "네": 4,
            "다섯": 5,
            "여섯": 6,
            "일곱": 7,
            "여덟": 8,
            "아홉": 9,
            "열": 10,
        }
        kor_num_pattern = "(" + "|".join(kor_num_map.keys()) + ")"

        for canonical, synonyms in self.food_vocab.items():
            candidates = set(synonyms) | {canonical}
            total_for_food = 0

            for cand in candidates:
                if not cand:
                    continue

                pattern_front = rf"(\d+)\s*{units}\s*{re.escape(cand)}"
                pattern_back = rf"{re.escape(cand)}\s*(\d+)\s*{units}"

                for m in re.finditer(pattern_front, text_clean):
                    num = int(m.group(1))
                    total_for_food += num

                for m in re.finditer(pattern_back, text_clean):
                    num = int(m.group(1))
                    total_for_food += num

                pattern_kor_back = rf"{re.escape(cand)}\s*{kor_num_pattern}\s*{units}"
                for m in re.finditer(pattern_kor_back, text_clean):
                    kor = m.group(1)
                    num = kor_num_map.get(kor, 1)
                    total_for_food += num

            if total_for_food == 0:
                if any(cand in text_clean for cand in candidates):
                    total_for_food = 1

            if total_for_food > 0:
                counts[canonical] = total_for_food

        if not counts:
            return counts

        result: dict[str, int] = {}
        for food in sorted(counts.keys(), key=len, reverse=True):
            if any(food in longer for longer in result.keys()):
                continue
            result[food] = counts[food]

        return result


if __name__ == "__main__":
    nutrition_db = NutritionDatabase()
    food_vocab = build_food_vocab_from_db(nutrition_db)

    print("=== NLP + Nutrition 데모 시작 ===")
    parser = FoodParser(food_vocab)
    print("=== FoodParser 준비 완료 ===")

    while True:
        try:
            text = input("먹은 음식을 입력하세요 (종료: q): ").strip()
        except EOFError:
            print("\nEOF 입력, 종료합니다.")
            break

        if text.lower() == "q":
            print("종료합니다.")
            break

        food_counts = parser.extract_food_counts(text)
        print("추출된 음식 및 개수:", food_counts)

        unknown_foods: list[tuple[str, int]] = []

        for food, cnt in food_counts.items():
            info = nutrition_db.get_nutrition(food)
            if info is not None:
                print(f" - {food} x{cnt}개 영양정보:", info)
            else:
                unknown_foods.append((food, cnt))

        if unknown_foods:
            names = [f"{name} x{cnt}개" for name, cnt in unknown_foods]
            joined = ", ".join(names)
            print(
                f"* 안내: 다음 음식은 영양 정보 DB에 없어 분석에서 제외되었습니다: {joined}"
            )

        print()
