from __future__ import annotations

from core.models import ValidationStatus
from state.workflow_state import WorkflowState


def after_validation_static(state: WorkflowState) -> str:
    vals = state.static_validation.validations
    if any(v.status in {ValidationStatus.FAILED, ValidationStatus.MISSING} for v in vals):
        return 'END_FAILURE'
    if any(v.status == ValidationStatus.ASSUMED for v in vals):
        return 'test-assumptions'
    if state.static_validation.overall_confidence < 0.85:
        return 'test-assumptions'
    return 'refactor-code-structure'


def after_validation_final(state: WorkflowState) -> str:
    vals = state.final_validation.validations
    if any(v.status in {ValidationStatus.FAILED, ValidationStatus.MISSING, ValidationStatus.MANUAL_REVIEW} for v in vals):
        return 'END_FAILURE'
    return 'refactor-code-structure'


def after_refactor(state: WorkflowState) -> str:
    mode = state.refactoring.refactor_mode.value
    if mode == 'blocked':
        return 'END_FAILURE'
    if mode == 'review':
        return 'HUMAN_REVIEW_GATE'
    return 'test-generate-suite'
