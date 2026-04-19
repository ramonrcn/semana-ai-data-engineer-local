import json
from itertools import islice
from collections import Counter

FILE_PATH = "gen/data/reviews/reviews.jsonl"


def analyze_reviews(**kwargs):
    samples = []
    sentiment_counter = Counter()
    rating_counter = Counter()

    with open(FILE_PATH, "r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            data = json.loads(line)

            # collect samples
            if i < 10:
                samples.append(data)

            # aggregate
            sentiment_counter[data["sentiment"]] += 1
            rating_counter[str(data["rating"])] += 1

    structure = list(samples[0].keys()) if samples else []

    return {
        "samples": samples,
        "structure": structure,
        "sentiment_distribution": dict(sentiment_counter),
        "rating_distribution": dict(rating_counter),
    }