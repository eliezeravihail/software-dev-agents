from __future__ import annotations

from statistics import mean
from core.models import ValidationOutput, ValidationStatus, RefactorMode, RiskLevel


def compute_validation_summary(output: ValidationOutput) -> dict[str, float | str]:
    confidences = [v.score.confidence for v in output.validations] or [0.0]
    failed = sum(v.status == ValidationStatus.FAILED for v in output.validations)
    assumed = sum(v.status == ValidationStatus.ASSUMED for v in output.validations)
    missing = sum(v.status == ValidationStatus.MISSING for v in output.validations)
    return {
        'overall_confidence': round(mean(confidences), 3),
        'failed_count': failed,
        'assumed_count': assumed,
        'missing_count': missing,
        'overall_risk': output.overall_risk.value,
    }


def choose_refactor_mode(confidence: float, risk: RiskLevel) -> RefactorMode:
    if risk == RiskLevel.HIGH or confidence < 0.70:
        return RefactorMode.BLOCKED
    if risk == RiskLevel.MEDIUM or confidence < 0.85:
        return RefactorMode.REVIEW
    return RefactorMode.AUTO
