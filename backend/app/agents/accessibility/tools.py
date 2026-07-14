from typing import Any


def get_boolean_value(
    project_data: dict[str, Any],
    field_name: str,
    default: bool = False,
) -> bool:
    """
    Read a boolean value safely from project data.
    """

    value = project_data.get(field_name, default)

    if isinstance(value, bool):
        return value

    if isinstance(value, int):
        return value == 1

    if isinstance(value, str):
        return value.strip().lower() in {
            "true",
            "yes",
            "1",
            "available",
            "provided",
        }

    return default


def get_numeric_value(
    project_data: dict[str, Any],
    field_name: str,
    default: float = 0.0,
) -> float:
    """
    Read a numeric value safely from project data.
    """

    value = project_data.get(field_name, default)

    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def calculate_accessibility_score(
    project_data: dict[str, Any],
) -> dict[str, Any]:
    """
    Calculate accessibility metrics using initial rule-based checks.

    These checks are preliminary and do not represent official
    legal or building-code compliance.
    """

    score = 40
    compliant_features: list[str] = []
    detected_issues: list[str] = []
    missing_information: list[str] = []

    has_step_free_entrance = get_boolean_value(
        project_data,
        "has_step_free_entrance",
    )

    has_accessible_route = get_boolean_value(
        project_data,
        "has_accessible_route",
    )

    has_ramp = get_boolean_value(
        project_data,
        "has_ramp",
    )

    has_elevator = get_boolean_value(
        project_data,
        "has_elevator",
    )

    has_accessible_parking = get_boolean_value(
        project_data,
        "has_accessible_parking",
    )

    has_accessible_bathroom = get_boolean_value(
        project_data,
        "has_accessible_bathroom",
    )

    has_wheelchair_turning_space = get_boolean_value(
        project_data,
        "has_wheelchair_turning_space",
    )

    has_handrails = get_boolean_value(
        project_data,
        "has_handrails",
    )

    has_accessible_emergency_exit = get_boolean_value(
        project_data,
        "has_accessible_emergency_exit",
    )

    door_width_cm = get_numeric_value(
        project_data,
        "door_width_cm",
    )

    corridor_width_cm = get_numeric_value(
        project_data,
        "corridor_width_cm",
    )

    ramp_slope_percent = get_numeric_value(
        project_data,
        "ramp_slope_percent",
    )

    floors = int(
        get_numeric_value(
            project_data,
            "floors",
            1,
        )
    )

    if has_step_free_entrance:
        score += 8
        compliant_features.append("Step-free entrance")
    else:
        detected_issues.append("No step-free entrance identified")

    if has_accessible_route:
        score += 8
        compliant_features.append("Accessible circulation route")
    else:
        detected_issues.append("No continuous accessible route identified")

    if has_ramp:
        score += 5
        compliant_features.append("Accessible ramp")
    else:
        detected_issues.append("No ramp identified for level changes")

    if floors > 1:
        if has_elevator:
            score += 10
            compliant_features.append("Elevator access between floors")
        else:
            score -= 10
            detected_issues.append(
                "Multi-floor building without an accessible elevator"
            )
    elif has_elevator:
        compliant_features.append("Elevator provided")

    if has_accessible_parking:
        score += 5
        compliant_features.append("Accessible parking")
    else:
        detected_issues.append("Accessible parking not identified")

    if has_accessible_bathroom:
        score += 7
        compliant_features.append("Accessible bathroom")
    else:
        detected_issues.append("Accessible bathroom not identified")

    if has_wheelchair_turning_space:
        score += 5
        compliant_features.append("Wheelchair turning space")
    else:
        detected_issues.append(
            "Wheelchair turning space not identified"
        )

    if has_handrails:
        score += 3
        compliant_features.append("Handrails provided")
    else:
        detected_issues.append("Handrails not identified")

    if has_accessible_emergency_exit:
        score += 5
        compliant_features.append("Accessible emergency egress")
    else:
        detected_issues.append(
            "Accessible emergency egress not identified"
        )

    if door_width_cm == 0:
        missing_information.append("Door width")
    elif door_width_cm >= 90:
        score += 5
        compliant_features.append(
            f"Door width: {door_width_cm:g} cm"
        )
    else:
        detected_issues.append(
            f"Door width may be insufficient: {door_width_cm:g} cm"
        )

    if corridor_width_cm == 0:
        missing_information.append("Corridor width")
    elif corridor_width_cm >= 120:
        score += 5
        compliant_features.append(
            f"Corridor width: {corridor_width_cm:g} cm"
        )
    else:
        detected_issues.append(
            f"Corridor width may be insufficient: "
            f"{corridor_width_cm:g} cm"
        )

    if has_ramp:
        if ramp_slope_percent == 0:
            missing_information.append("Ramp slope")
        elif ramp_slope_percent <= 8.33:
            score += 4
            compliant_features.append(
                f"Ramp slope: {ramp_slope_percent:g}%"
            )
        else:
            detected_issues.append(
                f"Ramp slope may be too steep: "
                f"{ramp_slope_percent:g}%"
            )

    score = max(0, min(round(score), 100))

    return {
        "score": score,
        "compliant_features": compliant_features,
        "detected_issues": detected_issues,
        "missing_information": missing_information,
        "measurements": {
            "door_width_cm": door_width_cm or None,
            "corridor_width_cm": corridor_width_cm or None,
            "ramp_slope_percent": ramp_slope_percent or None,
            "floors": floors,
        },
    }