from collections import defaultdict
from typing import Callable


def rrf_fuse(
    runs: list[list[dict]],
    key_fn: Callable[[dict], str],
    base_k: int = 60,
) -> list[tuple[str, float, list[dict]]]:
    scores: dict[str, float] = defaultdict(float)
    sources: dict[str, list[dict]] = defaultdict(list)

    for run in runs:
        weight = float(run[0].get("weight_used", 1.0)) if run else 1.0
        for rank, item in enumerate(run, start=1):
            key = key_fn(item)
            contribution = weight * (1.0 / (base_k + rank))
            scores[key] += contribution
            sources[key].append(
                {
                    **item,
                    "rank": rank,
                    "rrf_contribution": contribution,
                }
            )

    ordered = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return [(key, score, sources[key]) for key, score in ordered]
