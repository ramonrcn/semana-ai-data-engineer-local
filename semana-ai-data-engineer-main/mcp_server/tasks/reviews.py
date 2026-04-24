import json
from collections import Counter
from mcp_server.utils.formatters import format_reviews_analysis

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

    raw_data = { 
        "summary":{
        "samples": samples,
        "structure": structure,
        "sentiment_distribution": dict(sentiment_counter),
        "rating_distribution": dict(rating_counter),
        }
    }

    report = format_reviews_analysis(raw_data)

    return report