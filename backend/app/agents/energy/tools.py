from typing import Any


def to_float(
    value: Any,
    default: float = 0.0,
) -> float:
    try:
        return float(value)

    except (TypeError, ValueError):
        return default


def calculate_energy_score(project_data: dict) -> dict:
    score = 45
    observations = []

    insulation = str(
        project_data.get("insulation", "")
    ).lower()

    if insulation in {
        "good",
        "high",
        "excellent",
    }:
        score += 15
        observations.append(
            "Good insulation is indicated."
        )

    elif insulation in {
        "poor",
        "low",
    }:
        score -= 10
        observations.append(
            "Insulation may be insufficient."
        )

    glazing_type = str(
        project_data.get("glazing_type", "")
    ).lower()

    if glazing_type in {
        "double",
        "double glazing",
        "triple",
        "low-e",
    }:
        score += 10

    if project_data.get("shading_devices"):
        score += 10

    if project_data.get("solar_panels"):
        score += 10

    ratio = to_float(
        project_data.get("window_to_wall_ratio")
    )

    if 20 <= ratio <= 40:
        score += 10

    elif ratio > 60:
        score -= 10

    return {
        "energy_score": max(
            0,
            min(score, 100),
        ),
        "window_to_wall_ratio": ratio,
        "observations": observations,
    }