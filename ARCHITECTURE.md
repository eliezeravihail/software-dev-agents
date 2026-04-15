# Architecture — Production v2

## Pipeline
```
validate-requirements-static
    ↓ (ASSUMED or confidence < 0.85)
test-assumptions
    ↓
validate-requirements-final
    ↓
refactor-code-structure
    ↓ (auto only)
test-generate-suite
```

## Production controls added in v2
| Control | What it does |
|---------|-------------|
| Adaptive retry | Each retry changes strategy, not just reruns |
| Confidence scoring | Every node emits a 0.0–1.0 score |
| Risk scoring | low / medium / high per node |
| Refactor guardrails | auto / review / blocked based on score thresholds |
| Prompt versioning | Manifest-locked — deterministic across runs |
| Knowledge hygiene | Dedupe threshold, stale decay, quality ranking |

## Human review gate
The orchestrator must stop at the review gate when refactor_mode = review.
Only user-approved patches may be applied.
