import os
import json
from collections import Counter


def file_exists(path: str) -> bool:
    return os.path.exists(path)


def read_file(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def read_jsonl_sample(path: str, n: int = 100):
    data = []
    with open(path, "r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            if i >= n:
                break
            data.append(json.loads(line))
    return data


def analyze_reviews(data):
    sentiments = Counter()
    ratings = Counter()

    for r in data:
        sentiments[r["sentiment"]] += 1
        ratings[r["rating"]] += 1

    return sentiments, ratings