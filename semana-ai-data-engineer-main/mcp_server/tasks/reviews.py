import json
from itertools import islice
from collections import Counter
from mcp_server.logging_config import get_logger

logger = get_logger(__name__)

FILE_PATH = "gen/data/reviews/reviews.jsonl"

def reviews_analysis():
    path = FILE_PATH

    logger.info("[TRACE] reviews_analysis started")

    reviews = []
    sentiments = {}
    ratings = {}

    with open(path, "r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            data = json.loads(line)

            if i < 10:
                reviews.append(data)

            sentiment = data.get("sentiment")
            rating = data.get("rating")

            sentiments[sentiment] = sentiments.get(sentiment, 0) + 1
            ratings[rating] = ratings.get(rating, 0) + 1

    logger.info("[TRACE] reviews_analysis finished")

    return {
        "sample": reviews,
        "sentiment_dist": sentiments,
        "rating_dist": ratings,
    }


def reviews_summary():
    path = FILE_PATH

    logger.info("[TRACE] reviews_summary started")

    sample = []
    sentiments = {}
    ratings = {}

    with open(path, "r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            data = json.loads(line)

            if i < 10:
                sample.append(data)

            s = data.get("sentiment")
            r = data.get("rating")

            sentiments[s] = sentiments.get(s, 0) + 1
            ratings[r] = ratings.get(r, 0) + 1

    logger.info("[TRACE] reviews_summary finished")

    return {
        "sample": sample,
        "sentiment_dist": sentiments,
        "rating_dist": ratings,
        "structure": list(sample[0].keys()) if sample else [],
    }


def analyze_reviews_task():
    logger.info("[TASK] analyze_reviews started")

    samples = []
    sentiments = Counter()
    ratings = Counter()

    try:
        with open(FILE_PATH, "r", encoding="utf-8") as f:
            lines = list(islice(f, 1000))  # safe cap

        for i, line in enumerate(lines):
            data = json.loads(line)

            if i < 10:
                samples.append(data)

            sentiments[data.get("sentiment")] += 1
            ratings[data.get("rating")] += 1

        result = {
            "sample_reviews": samples,
            "structure": list(samples[0].keys()) if samples else [],
            "sentiment_distribution": dict(sentiments),
            "rating_distribution": dict(ratings),
        }

        logger.info("[TASK] analyze_reviews completed")

        return result

    except Exception as e:
        logger.exception("[TASK] analyze_reviews failed")
        raise e