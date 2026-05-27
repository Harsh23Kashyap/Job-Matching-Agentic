from core.lexical import LexicalRanker


def _sample_jobs():
    return [
        {
            "id": "job_ml",
            "title": "Machine Learning Engineer",
            "required_skills": ["Python", "Machine Learning"],
            "required_experience": 2,
            "description": "Build ML models with Python.",
            "remote_policy": True,
        },
        {
            "id": "job_fe",
            "title": "Frontend Developer",
            "required_skills": ["React", "JavaScript"],
            "required_experience": 1,
            "description": "Build React UIs.",
            "remote_policy": True,
        },
    ]


def test_lexical_bm25_ranks_ml_job_for_ml_resume():
    ranker = LexicalRanker(_sample_jobs())
    resume = {
        "name": "Alex",
        "skills": ["Python", "Machine Learning", "TensorFlow"],
        "experience_years": 3,
        "summary": "ML engineer with Python experience.",
        "remote_preference": True,
    }
    ranked = ranker.rank_jobs(resume, "bm25", top_k=2)
    assert ranked[0][0] == "job_ml"
    assert ranked[0][1] > 0


def test_lexical_tfidf_returns_scores():
    ranker = LexicalRanker(_sample_jobs())
    resume = {
        "name": "Sam",
        "skills": ["React", "JavaScript"],
        "experience_years": 2,
        "summary": "Frontend developer.",
        "remote_preference": True,
    }
    ranked = ranker.rank_jobs(resume, "tfidf", top_k=1)
    assert len(ranked) == 1
    assert ranked[0][0] in {"job_ml", "job_fe"}


def test_lexical_unknown_method_raises():
    ranker = LexicalRanker(_sample_jobs())
    try:
        ranker.rank_jobs({"name": "x", "skills": []}, "unknown", top_k=1)
        raised = False
    except ValueError as exc:
        raised = True
        assert "Unknown lexical method" in str(exc)
    assert raised
