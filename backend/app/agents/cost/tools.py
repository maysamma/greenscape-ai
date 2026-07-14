from typing import Any


def to_float(
    value: Any,
    default: float = 0.0,
) -> float:
    try:
        return float(value)

    except (TypeError, ValueError):
        return default


def estimate_project_cost(
    project_data: dict,
) -> dict:
    area = to_float(
        project_data.get("built_up_area_m2")
    )

    cost_per_meter = to_float(
        project_data.get(
            "cost_per_square_meter_sar",
            2500,
        )
    )

    complexity = str(
        project_data.get(
            "design_complexity",
            "medium",
        )
    ).lower()

    multiplier = 1.0

    if complexity == "high":
        multiplier = 1.20

    elif complexity == "low":
        multiplier = 0.90

    estimated_cost = (
        area
        * cost_per_meter
        * multiplier
    )

    return {
        "built_up_area_m2": area,
        "cost_per_square_meter_sar": cost_per_meter,
        "complexity_multiplier": multiplier,
        "estimated_cost_sar": round(
            estimated_cost,
            2,
        ),
        "confidence": (
            "medium"
            if area > 0
            else "low"
        ),
        "disclaimer": (
            "This is an early conceptual estimate."
        ),
    }