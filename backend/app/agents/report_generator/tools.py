from typing import Any


SCORE_KEYS = {
    "architecture_review": [
        "architecture_score",
        "score",
    ],
    "sustainability": [
        "sustainability_score",
        "score",
    ],
    "energy": [
        "energy_score",
        "score",
    ],
    "ventilation": [
        "ventilation_score",
        "score",
    ],
    "lighting": [
        "lighting_score",
        "score",
    ],
    "accessibility": [
        "accessibility_score",
        "score",
    ],
    "building_code": [
        "code_score",
        "score",
    ],
}


def find_score(
    data: Any,
    keys: list[str],
) -> float | None:
    if not isinstance(data, dict):
        return None

    for key in keys:
        value = data.get(key)

        if isinstance(value, (int, float)):
            return float(value)

    for value in data.values():
        if isinstance(value, dict):
            score = find_score(
                value,
                keys,
            )

            if score is not None:
                return score

    return None


def get_rating(score: float) -> str:
    if score >= 90:
        return "Excellent"

    if score >= 80:
        return "Very Good"

    if score >= 70:
        return "Good"

    if score >= 50:
        return "Fair"

    return "Poor"


def calculate_overall_score(
    agent_results: dict,
) -> dict:
    category_scores = {}

    for agent_name, keys in SCORE_KEYS.items():
        result = agent_results.get(
            agent_name,
            {},
        )

        score = find_score(
            result,
            keys,
        )

        if score is not None:
            category_scores[agent_name] = max(
                0,
                min(score, 100),
            )

    overall_score = (
        round(
            sum(category_scores.values())
            / len(category_scores),
            2,
        )
        if category_scores
        else 0
    )

    return {
        "overall_score": overall_score,
        "overall_rating": get_rating(
            overall_score
        ),
        "category_scores": category_scores,
        "agents_included": len(
            category_scores
        ),
    }