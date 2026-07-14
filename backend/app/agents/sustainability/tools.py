def calculate_sustainability_score(
    project_data: dict,
) -> dict:
    score = 35
    observations = []

    features = {
        "solar_panels": 12,
        "green_space": 10,
        "rainwater_collection": 10,
        "water_saving_fixtures": 8,
        "recycled_materials": 8,
        "local_materials": 7,
        "natural_ventilation": 5,
        "natural_lighting": 5,
    }

    detected_features = []

    for feature, points in features.items():
        if project_data.get(feature):
            score += points
            detected_features.append(feature)

    if detected_features:
        observations.append(
            "The project includes sustainable design features."
        )

    return {
        "sustainability_score": max(
            0,
            min(score, 100),
        ),
        "detected_features": detected_features,
        "observations": observations,
    }