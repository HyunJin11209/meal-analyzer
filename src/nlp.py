# src/nlp.py

from typing import Dict, List, Set
from transformers import AutoTokenizer

print("DEBUG: 코드 실행됨")


def _normalize(text: str) -> str:
    """공백 제거 + 소문자로 통일 (매칭용)."""
    return text.replace(" ", "").lower()


class FoodParser:
    """
    HuggingFace 토크나이저를 사용해서
    문장에서 음식 이름(표준 이름)을 뽑아오는 간단한 파서.
    """

    def __init__(self, food_vocab: Dict[str, List[str]]) -> None:
        """
        food_vocab 예시:
        {
            "라면": ["라면", "봉지라면", "컵라면"],
            "햄버거": ["햄버거", "버거"],
            ...
        }
        """
        print("DEBUG 3: 토크나이저 로딩 시작")
        self.tokenizer = AutoTokenizer.from_pretrained("klue/bert-base")
        print("DEBUG 4: 토크나이저 로딩 완료")

        # "정규화된 표현" -> "표준 음식 이름" 매핑
        self.synonym_to_canonical: Dict[str, str] = {}
        for canonical, syn_list in food_vocab.items():
            # 표준 이름도 포함해서 모두 매핑
            all_forms = set(syn_list) | {canonical}
            for form in all_forms:
                key = _normalize(form)
                self.synonym_to_canonical[key] = canonical

    def extract_food_names(self, text: str) -> List[str]:
        """
        문장에서 음식 이름(표준 이름 기준)만 리스트로 추출.
        지금은 단순히 '동의어 문자열이 문장 안에 포함되어 있는지'로 검사.
        (나중에 토큰/형태소 기반으로 고도화 가능)
        """
        print("[DEBUG] extract_food_names 호출:", text)

        found: Set[str] = set()
        norm_text = _normalize(text)

        for norm_synonym, canonical in self.synonym_to_canonical.items():
            if norm_synonym in norm_text:
                found.add(canonical)

        return sorted(found)


if __name__ == "__main__":
    # 예시용 vocab (나중에 JSON/DB에서 불러오도록 수정 예정)
    example_vocab = {
        "라면": ["라면", "봉지라면", "컵라면"],
        "삼각김밥": ["삼각김밥", "삼각 김밥"],
        "햄버거": ["햄버거", "버거"],
        "피자": ["피자"],
    }

    print("=== NLP 데모 시작 ===")
    parser = FoodParser(example_vocab)
    print("=== FoodParser 준비 완료 ===")

    while True:
        try:
            text = input("먹은 음식을 입력하세요 (종료: q): ").strip()
        except EOFError:
            # 터미널에서 Ctrl+Z 같은 걸로 종료될 때 대비
            print("\nEOF 입력, 종료합니다.")
            break

        if text.lower() == "q":
            print("종료합니다.")
            break

        foods = parser.extract_food_names(text)
        print("추출된 음식:", foods)
        print()
