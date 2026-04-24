def format_business_analysis(data: dict) -> str:
    lines = []

    # --- COUNTS ---
    counts = data["counts"]
    lines.append("📊 COUNTS")
    lines.append(f"- Customers: {counts['customers']}")
    lines.append(f"- Products: {counts['products']}")
    lines.append(f"- Orders: {counts['orders']}")
    lines.append("")

    # --- CUSTOMERS SAMPLE ---
    lines.append("👥 SAMPLE CUSTOMERS")
    for i, c in enumerate(data["customers_sample"], 1):
        lines.append(
            f"{i}. {c['name']} ({c['state']}, {c['segment']})"
        )
    lines.append("")

    # --- ORDERS SAMPLE ---
    lines.append("📦 SAMPLE ORDERS")
    for i, o in enumerate(data["orders_sample"], 1):
        lines.append(
            f"{i}. ${o['total']:.2f} | {o['status']} | {o['payment']}"
        )
    lines.append("")

    # --- ORDER DISTRIBUTION ---
    lines.append("📈 ORDERS BY STATUS")
    for row in data["orders_distribution"]:
        lines.append(
            f"- {row['status']}: {row['count']} ({row['percentage']}%)"
        )
    lines.append("")

    # --- CUSTOMERS BY STATE ---
    lines.append("🌎 CUSTOMERS BY STATE")
    for row in data["customers_by_state"]:
        lines.append(
            f"- {row['state']}: {row['count']} ({row['percentage']}%)"
        )

    return "\n".join(lines)

def format_reviews_analysis(data: dict) -> str:
    lines = []

    summary = data["summary"]

    # --- STRUCTURE ---
    lines.append("🧾 REVIEW STRUCTURE")
    lines.append(", ".join(summary["structure"]))
    lines.append("")

    # --- SENTIMENT ---
    lines.append("📊 SENTIMENT DISTRIBUTION")
    for k, v in summary["sentiment_distribution"].items():
        lines.append(f"- {k}: {v}")
    lines.append("")

    # --- RATINGS ---
    lines.append("⭐ RATING DISTRIBUTION")
    for k, v in sorted(summary["rating_distribution"].items()):
        lines.append(f"- {k}: {v}")
    lines.append("")

    # --- SAMPLE REVIEWS ---
    lines.append("💬 SAMPLE REVIEWS")
    for r in summary["samples"]:
        lines.append(
            f"- ({r['rating']}⭐ | {r['sentiment']}) {r['comment']}"
        )

    return "\n".join(lines)