---
description: "Agent 1 — guarded structural refactor with diff impact and approval mode"
allowed-tools: Read, Write, Edit
---

1. Read `agents/prompts/prompt_versions.yaml`
2. Load the Agent 1 version defined there

## Guardrails
- `auto`    — confidence >= 0.85 AND risk = low  → apply changes
- `review`  — confidence 0.70–0.84 OR risk = medium → show patch only, do NOT apply silently
- `blocked` — confidence < 0.70 OR risk = high  → explain only, no code output

## Required output
REFACTOR_MODE + AGGREGATE_CONFIDENCE + AGGREGATE_RISK
Per change: description + pattern + risk + reversible + diff (+N/-M lines) + api_changed
BEHAVIOR_GUARANTEE
REFACTORED_CODE (if auto or review)
