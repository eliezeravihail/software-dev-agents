# software-dev-agents

## Always-active rules
- Always read `agents/prompts/prompt_versions.yaml` before invoking any agent, then load the exact versioned prompt file listed there.
- Validation uses three channels: static analysis + semantic validation + confidence scoring.
- Refactor changes are gated by `refactor_mode` (auto / review / blocked).
- BOOKS knowledge is loaded by `quality_score` descending; skip `stale=true` entries.

## BOOKS knowledge base path
BOOKS skill files live in the companion repo. Point `BooksLoaderTool(books_root=...)` to:
`C:\Users\eliezera\Projects\knowledge-library-agents\skills\BOOKS`
If the path does not exist, run `git clone` of knowledge-library-agents first.

## Agent map
| Agent | Role | Model |
|-------|------|-------|
| refactorer | Refactoring + Guardrails | claude-sonnet-4-6 |
| validator  | Validation + Scoring      | claude-sonnet-4-6, temp=0 |
| tester     | Testing + Coverage        | claude-sonnet-4-6 |

## Primary entrypoints
- `/project:dev-cycle`                   — full adaptive pipeline
- `/project:validate-requirements-static`— static + semantic validation
- `/project:test-assumptions`            — targeted falsification tests
- `/project:validate-requirements-final` — final validation with test evidence
- `/project:refactor-code-structure`     — guarded refactor
- `/project:test-generate-suite`         — pytest suite + coverage score
