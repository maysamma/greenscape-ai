from typing import Any


def to_float(
    value: Any,
    default: float = 0.0,
) -> float:
    try:
        return float(value)

    except (TypeError, ValueError):
        return default


def to_int(
    value: Any,
    default: int = 0,
) -> int:
    try:
        return int(value)

    except (TypeError, ValueError):
        return default


def run_basic_code_checks(
    project_data: dict,
) -> dict:
    checks = []
    missing_information = []

    exits_count = to_int(
        project_data.get("exits_count")
    )

    if exits_count <= 0:
        missing_information.append(
            "Number of exits"
        )

    else:
        checks.append(
            {
                "check": "Emergency exits",
                "passed": exits_count >= 1,
                "value": exits_count,
            }
        )

    door_width = to_float(
        project_data.get("minimum_door_width_cm")
    )

    if door_width <= 0:
        missing_information.append(
            "Minimum door width"
        )

    else:
        checks.append(
            {
                "check": "Door width",
                "passed": door_width >= 80,
                "value": door_width,
                "unit": "cm",
            }
        )

    corridor_width = to_float(
        project_data.get("minimum_corridor_width_cm")
    )

    if corridor_width <= 0:
        missing_information.append(
            "Minimum corridor width"
        )

    else:
        checks.append(
            {
                "check": "Corridor width",
                "passed": corridor_width >= 90,
                "value": corridor_width,
                "unit": "cm",
            }
        )

    if not project_data.get("building_type"):
        missing_information.append(
            "Building type"
        )

    if not project_data.get("location"):
        missing_information.append(
            "Project location"
        )

    if not project_data.get("applicable_code"):
        missing_information.append(
            "Applicable building code"
        )

    passed = sum(
        1
        for check in checks
        if check["passed"]
    )

    score = (
        round(
            (passed / len(checks)) * 100,
            2,
        )
        if checks
        else 0
    )

    return {
        "code_score": score,
        "checks": checks,
        "missing_information": missing_information,
        "disclaimer": (
            "This is a preliminary review and not official approval."
        ),
    }