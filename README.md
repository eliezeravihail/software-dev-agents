# software-dev-agents

Claude Code plugin — multi-agent pipeline for professional code development.

## Agents
| Agent | Role | Model |
|-------|------|-------|
| Agent 1 | Refactoring + Guardrails | Sonnet |
| Agent 2 | Validation + Scoring | Sonnet, temp=0 |
| Agent 3 | Testing + Coverage | Sonnet |

## Commands
| Command | What it does |
|---------|-------------|
| `/project:dev-cycle` | Full adaptive pipeline: validate → test → refactor → coverage |
| `/project:validate-requirements-static` | Static + semantic validation with scoring |
| `/project:test-assumptions` | Targeted falsification tests for assumed items |
| `/project:validate-requirements-final` | Final validation with test evidence |
| `/project:refactor-code-structure` | Guarded refactor (auto / review / blocked) |
| `/project:test-generate-suite` | pytest suite + coverage score |

## Refactor modes
| Mode | Condition | Behavior |
|------|-----------|----------|
| `auto` | confidence >= 0.85, risk = low | Changes applied automatically |
| `review` | confidence 0.70–0.84 or risk = medium | Patch shown — waits for approval |
| `blocked` | confidence < 0.70 or risk = high | Explanation only, no changes |

## Install
1. Clone this repo into your project root
2. Open the folder in Claude Code
3. Run `/project:dev-cycle`

## Knowledge base
This plugin can load BOOKS context from the companion repo
[knowledge-library-agents](https://github.com/eliezeravihail/knowledge-library-agents).
Point `BooksLoaderTool(books_root=...)` to its `skills/BOOKS/` folder.
