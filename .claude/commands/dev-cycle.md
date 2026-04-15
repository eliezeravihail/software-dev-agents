---
description: "Full adaptive pipeline: validate → test → validate → refactor → coverage"
allowed-tools: Read, Write, Bash
---

Read `agents/prompts/prompt_versions.yaml` before each step.

## State graph
```
START
  → validate-requirements-static
      FAILED / MISSING                  → END_FAILURE
      ASSUMED or confidence < 0.85      → test-assumptions
                                        → validate-requirements-final
      all verified + confidence >= 0.85 → refactor-code-structure

  → refactor-code-structure
      blocked  → END_FAILURE
      review   → show patch, wait for user approval, then continue
      auto     → test-generate-suite → END_SUCCESS
```

## Adaptive retry (max 3 attempts per step)
- Attempt 1: standard prompt
- Attempt 2: prepend "Previous attempt failed with: <error>. Focus only on that issue."
- Attempt 3: prepend "Reduce scope to one requirement at a time. Return structured output only."

## Metrics to collect per node
- confidence_score
- risk_score
- latency_ms
- diff_impact (refactor only: +lines, -lines, api_changed)

Each step runs as: `claude --print < <prompt_file>`
