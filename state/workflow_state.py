from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any
from core.api_models import DevelopmentTask
from core.models import RefactorMode


@dataclass
class WorkflowState:
    task: DevelopmentTask
    status: str = 'created'
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    static_validation: Any | None = None
    assumption_tests: Any | None = None
    final_validation: Any | None = None
    refactoring: Any | None = None
    coverage: Any | None = None
    node_attempts: dict[str, int] = field(default_factory=dict)
    node_scores: dict[str, dict[str, float | str]] = field(default_factory=dict)
    prompt_versions: dict[str, str] = field(default_factory=dict)
    approval_mode: RefactorMode = RefactorMode.REVIEW
    errors: list[dict[str, str]] = field(default_factory=list)
    events: list[dict[str, Any]] = field(default_factory=list)

    def log_event(self, node: str, message: str, **extra: Any) -> None:
        self.events.append({
            'ts': datetime.utcnow().isoformat(),
            'node': node,
            'message': message,
            **extra,
        })

    def log_error(self, node: str, error: Exception, attempt: int) -> None:
        self.errors.append({
            'ts': datetime.utcnow().isoformat(),
            'node': node,
            'attempt': str(attempt),
            'type': type(error).__name__,
            'message': str(error),
        })
