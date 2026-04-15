---
description: "Agent 3 coverage mode — full pytest suite with coverage score"
allowed-tools: Read, Write
---

1. Read `agents/prompts/prompt_versions.yaml`
2. Load the Agent 3 version defined there
3. Run in `coverage` mode

## Mandatory order
1. Build coverage matrix
2. Compute coverage_score
3. List uncovered requirements
4. Generate pytest suite after the matrix

## Required output
COVERAGE_MATRIX + COVERAGE_SCORE + UNCOVERED list + PYTEST_SUITE
