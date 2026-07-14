from typing import Any


def to_float(
    value: Any,
    default: float = 0.0,
) -> float:
    try:
        return float(value)

    except (TypeError, ValueError):
        return default


def calculate_space_efficiency(project_data: dict) -> dict:
    total_area = to_float(
        project_data.get("total_area_m2")
    )

    usable_area = to_float(
        project_data.get("usable_area_m2")
    )

    if total_area <= 0:
        efficiency = 0.0

    else:
        efficiency = round(
            (usable_area / total_area) * 100,
            2,
        )

    if efficiency >= 80:
        score = 90

    elif efficiency >= 70:
        score = 80

    elif efficiency >= 60:
        score = 70

    elif efficiency > 0:
        score = 50

    else:
        score = 0

    return {
        "architecture_score": score,
        "total_area_m2": total_area,
        "usable_area_m2": usable_area,
        "space_efficiency_percentage": efficiency,
    }