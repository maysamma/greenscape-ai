from typing import Any


def to_int(
    value: Any,
    default: int = 0,
) -> int:
    try:
        return int(value)

    except (TypeError, ValueError):
        return default


def calculate_ventilation_score(
    project_data: dict,
) -> dict:
    score = 40
    observations = []

    windows_count = to_int(
        project_data.get("windows_count")
    )

    if windows_count >= 8:
        score += 15

    elif windows_count <= 2:
        score -= 10

    if project_data.get("opposite_openings"):
        score += 20
        observations.append(
            "Opposite openings support cross ventilation."
        )

    if project_data.get("courtyard"):
        score += 10

    if project_data.get("operable_windows"):
        score += 10

    if project_data.get("kitchen_exhaust"):
        score += 5

    if project_data.get("bathroom_exhaust"):
        score += 5

    return {
        "ventilation_score": max(
            0,
            min(score, 100),
        ),
        "windows_count": windows_count,
        "cross_ventilation": bool(
            project_data.get("opposite_openings")
        ),
        "observations": observations,
    }