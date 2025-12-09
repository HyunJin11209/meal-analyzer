import json
import os

# 프로젝트 기준 경로 자동 계산
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "data.json")


def load_database():
    """DB 파일을 불러와서 dict로 반환"""
    if not os.path.exists(DB_PATH):
        # 파일 없으면 기본 구조 생성
        save_database({})
        return {}

    with open(DB_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_database(data: dict):
    """dict 데이터를 JSON으로 저장"""
    with open(DB_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def add_item(key, value):
    """DB에 데이터 추가"""
    data = load_database()
    data[key] = value
    save_database(data)


def delete_item(key):
    """DB에서 항목 삭제"""
    data = load_database()
    if key in data:
        del data[key]
        save_database(data)


def get_item(key):
    """키 값 하나 조회"""
    data = load_database()
    return data.get(key)
