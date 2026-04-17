import json
from mcp_server.services.files import read_jsonl_sample, analyze_reviews

def reviews_analysis():
    path = "gen/data/reviews/reviews.jsonl"

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

    return {
        "sample": reviews,
        "sentiment_dist": sentiments,
        "rating_dist": ratings,
    }

def reviews_summary():
    path = "gen/data/reviews/reviews.jsonl"

    sample = []
    sentiments = {}
    ratings = {}

    with open(path, "r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            data = json.loads(line)

            # sample 10
            if i < 10:
                sample.append(data)

            # distribution
            s = data.get("sentiment")
            r = data.get("rating")

            sentiments[s] = sentiments.get(s, 0) + 1
            ratings[r] = ratings.get(r, 0) + 1

    return {
        "sample": sample,
        "sentiment_dist": sentiments,
        "rating_dist": ratings,
        "structure": list(sample[0].keys()) if sample else []
    }

def analyze_reviews_task():
    path = "gen/data/reviews/reviews.jsonl"

    sample = read_jsonl_sample(path, 100)

    structure = list(sample[0].keys())

    sentiments, ratings = analyze_reviews(sample)

    return {
        "sample": sample[:10],
        "structure": structure,
        "sentiments": dict(sentiments),
        "ratings": dict(ratings),
    }