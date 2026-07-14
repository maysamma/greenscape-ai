from typing import Any


def to_float(
    value: Any,
    default: float = 0.0,
) -> float:
    try:
        return float(value)

    except (TypeError, ValueError):
        return default


def calculate_lighting_score(
    project_data: dict,
) -> dict:
    score = 40

    window_area = to_float(
        project_data.get("window_area_m2")
    )

    floor_area = to_float(
        project_data.get("floor_area_m2")
    )

    ratio = 0.0

    if floor_area > 0:
        ratio = (
            window_area / floor_area
        ) * 100

        if 10 <= ratio <= 25:
            score += 25

        elif ratio < 5:
            score -= 15

        elif ratio > 35:
            score -= 5

    if project_data.get("skylights"):
        score += 10

    if project_data.get("courtyard"):
        score += 10

    if project_data.get("shading_devices"):
        score += 10

    rooms_without_windows = project_data.get(
        "internal_rooms_without_windows",
        [],
    )

    if rooms_without_windows:
        score -= min(
            len(rooms_without_windows) * 5,
            20,
        )

    return {
        "lighting_score": max(
            0,
            min(round(score, 2), 100),
        ),
        "window_to_floor_ratio": round(
            ratio,
            2,
        ),
        "rooms_without_windows": rooms_without_windows,
    }