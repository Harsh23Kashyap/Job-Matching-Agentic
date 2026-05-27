from contracts.matching import MatchRequest


def test_rahul_sharma_ml_engineer_rank_one(system):
    req = MatchRequest(
        query_key="Rahul Sharma",
        top_k=5,
        strategy="semantic",
        metric="cosine",
    )
    response = system.matchmaker.match_candidate_to_jobs(req)
    assert response.results
    assert response.results[0].target_label == "Machine Learning Engineer"
    assert response.results[0].rank == 1


def test_job_to_candidates_reverse(system):
    req = MatchRequest(
        query_key="Machine Learning Engineer",
        top_k=5,
        strategy="semantic",
        metric="cosine",
    )
    response = system.matchmaker.match_job_to_candidates(req)
    assert response.direction == "job_to_candidates"
    assert len(response.results) == 5


def test_skills_mode_embedding_changes_scores(system):
    base = MatchRequest(
        query_key="Rahul Sharma",
        top_k=5,
        strategy="multimodal",
        metric="cosine",
        skills_mode="jaccard",
        semantic_weight=0.5,
    )
    embed = base.model_copy(update={"skills_mode": "embedding"})
    r1 = system.matchmaker.match_candidate_to_jobs(base)
    r2 = system.matchmaker.match_candidate_to_jobs(embed)
    assert r1.results[0].skills_score != r2.results[0].skills_score
