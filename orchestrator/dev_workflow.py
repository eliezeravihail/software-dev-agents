from __future__ import annotations

from core.api_models import DevelopmentResult, DevelopmentTask
from core.scoring import compute_validation_summary
from orchestrator.router import after_validation_final, after_validation_static, after_refactor
from state.workflow_state import WorkflowState


class DevWorkflowOrchestrator:
    """
    Reference implementation of the dev-cycle state graph.

    Design note
    -----------
    This class documents the workflow logic (state transitions, routing,
    scoring) but is NOT the runtime entrypoint. The actual execution runs
    inside Claude Code via the /project:dev-cycle slash command, which
    spawns each agent as an isolated subprocess with `claude --print`.

    To run the workflow: open this repo in Claude Code and use
        /project:dev-cycle
    """

    def __init__(self, router=None):
        self.router = router

    async def run(self, task: DevelopmentTask) -> DevelopmentResult:
        raise NotImplementedError(
            "Direct Python execution is not supported. "
            "Open this repo in Claude Code and run /project:dev-cycle."
        )

    @staticmethod
    def score_validation(state: WorkflowState, node: str) -> None:
        payload = state.static_validation if node == 'static' else state.final_validation
        if payload:
            state.node_scores[node] = compute_validation_summary(payload)
