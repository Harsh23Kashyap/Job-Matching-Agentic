from core.rrf import rrf_fuse


def test_rrf_fuse_combines_ranks():
    runs = [
        [
            {"target_id": "a", "score": 0.9, "strategy": "semantic", "metric": "cosine", "weight": 1.0, "weight_used": 1.0},
            {"target_id": "b", "score": 0.8, "strategy": "semantic", "metric": "cosine", "weight": 1.0, "weight_used": 1.0},
        ],
        [
            {"target_id": "b", "score": 0.95, "strategy": "multimodal", "metric": "cosine", "weight": 1.0, "weight_used": 1.0},
            {"target_id": "a", "score": 0.7, "strategy": "multimodal", "metric": "cosine", "weight": 1.0, "weight_used": 1.0},
        ],
    ]
    fused = rrf_fuse(runs, key_fn=lambda item: item["target_id"], base_k=60)
    assert fused[0][0] in {"a", "b"}
    assert len(fused) == 2


def test_rrf_empty_runs():
    assert rrf_fuse([], key_fn=lambda x: x) == []
