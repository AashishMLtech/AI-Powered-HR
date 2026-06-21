from app.services.scoring_service import compute_combined_score


def test_combined_score_uses_70_15_15_weights():
    assert compute_combined_score(80, 60, 40) == 71


def test_missing_linkedin_score_counts_as_zero():
    assert compute_combined_score(80, 60, None) == 65
