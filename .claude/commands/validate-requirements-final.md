---
description: "Validator Phase 2 — merge test evidence into final validation scores"
allowed-tools: Read, Write
---

1. Read `agents/prompts/prompt_versions.yaml`
2. Load the Validator version defined there

## Input
- Previous validation report
- test_results from test-assumptions

## Output
- Only requirements whose status changed
- Updated CONFIDENCE / RISK / EVIDENCE_STRENGTH per changed item
- Updated OVERALL_CONFIDENCE and OVERALL_RISK
