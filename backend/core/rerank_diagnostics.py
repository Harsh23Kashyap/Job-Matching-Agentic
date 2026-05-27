"""Helpers for cross-encoder rerank diagnostics."""
from __future__ import annotations

from contracts.matching import RankChange


def top_k_ids(scored: list, top_k: int, *, entity_index: int = 0) -> list[str]:
    """Extract entity ids from ranked rows like (entity, score, ...) or (id, score)."""
    ids: list[str] = []
    for row in scored[:top_k]:
        if isinstance(row, tuple):
            item = row[entity_index]
        else:
            item = row
        if isinstance(item, str):
            ids.append(item)
        else:
            ids.append(item.id)
    return ids


def compute_rank_changes(
    before_ids: list[str],
    after_ids: list[str],
    labels: dict[str, str],
    *,
    top_k: int,
) -> list[RankChange]:
    """Diff top-K order before vs after cross-encoder rerank."""
    changes: list[RankChange] = []
    universe = list(dict.fromkeys(before_ids + after_ids))
    for target_id in universe:
        rank_before = before_ids.index(target_id) + 1 if target_id in before_ids else None
        rank_after = after_ids.index(target_id) + 1 if target_id in after_ids else None
        if rank_before == rank_after:
            continue
        moved = None
        if rank_before is not None and rank_after is not None:
            moved = rank_after - rank_before
        changes.append(
            RankChange(
                target_id=target_id,
                target_label=labels.get(target_id, target_id),
                rank_before=rank_before,
                rank_after=rank_after,
                moved=moved,
            )
        )
    changes.sort(
        key=lambda c: (
            c.rank_after if c.rank_after is not None else top_k + 1,
            c.rank_before if c.rank_before is not None else top_k + 1,
        )
    )
    return changes
