---
description: "Agent 2 Phase 1 — static + semantic validation with confidence scoring"
allowed-tools: Read, Write
---

1. Read `agents/prompts/prompt_versions.yaml`
2. Load the Agent 2 version defined there
3. Validate every requirement through all three channels: static + semantic + scoring

## Required input
- Source file (path or content)
- Requirements list (requirement_id + text)
- BOOKS refs (optional)

## Required output
Per requirement: STATUS + CONFIDENCE + RISK + EVIDENCE_STRENGTH + EVIDENCE
For ASSUMED items: full TEST_REQUEST
At end: OVERALL_CONFIDENCE + OVERALL_RISK

## Routing after
- Any FAILED / MISSING → stop immediately
- confidence < 0.85 or any ASSUMED → run test-assumptions
- All verified + confidence >= 0.85 → run refactor-code-structure
