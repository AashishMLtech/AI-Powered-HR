def compute_combined_score(
    cv_score: float,
    github_score: float,
    linkedin_score: float | None = None,
) -> float:
    linkedin_value = linkedin_score if linkedin_score is not None else 0
    return round((cv_score * 0.70) + (github_score * 0.15) + (linkedin_value * 0.15), 2)
