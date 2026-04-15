---
description: "Agent 3 validation mode — targeted falsification tests for ASSUMED items"
allowed-tools: Read, Write
---

1. Read `agents/prompts/prompt_versions.yaml`
2. Load the Agent 3 version defined there
3. Run in `validation` mode

## Input
- TEST_REQUESTS from the previous validation step (ASSUMED items only)
- Source code

## Rules
- 1–2 tests per assumption only
- Goal is falsification, not confirmation
- Every result must include: passed/failed/null + confidence + evidence
