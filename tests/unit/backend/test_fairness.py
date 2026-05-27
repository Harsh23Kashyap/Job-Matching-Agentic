from core.fairness import disparate_impact_ratio, evaluate_fairness_report, experience_group, top_k_selection_rate


def test_experience_group_buckets():
    assert experience_group(1.0) == "junior"
    assert experience_group(3.0) == "mid"
    assert experience_group(8.0) == "senior"


def test_disparate_impact_ratio_parity():
    rates = {"a": 0.8, "b": 0.8}
    assert disparate_impact_ratio(rates) == 1.0


def test_evaluate_fairness_report_shape():
    ranked = {
        "cv_01": [("job_01", 0.9), ("job_02", 0.5)],
        "cv_02": [("job_02", 0.85), ("job_01", 0.4)],
    }
    meta = {
        "cv_01": {"experience_years": 1, "remote_preference": True},
        "cv_02": {"experience_years": 6, "remote_preference": False},
    }
    report = evaluate_fairness_report(ranked, meta)
    assert "experience_groups" in report
    assert "remote_groups" in report
    assert "experience_disparate_impact" in report


def test_top_k_selection_rate():
    ranked = {"q1": [("j1", 0.9)], "q2": [("j2", 0.1)]}
    groups = {"q1": "a", "q2": "b"}
    rates = top_k_selection_rate(ranked, groups, top_k=1)
    assert "a" in rates and "b" in rates
