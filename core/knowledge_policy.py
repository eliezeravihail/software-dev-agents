from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class KnowledgePolicy:
    duplicate_similarity_threshold: float = 0.80
    stale_days: int = 540
    replacement_margin: float = 0.10
    min_quality_score: float = 0.60


DEFAULT_KNOWLEDGE_POLICY = KnowledgePolicy()
