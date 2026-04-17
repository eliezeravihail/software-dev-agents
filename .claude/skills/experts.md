# Experts Router

You are the entry point for the software-dev-agents pipeline.
The user invoked `/experts` with a free-text request (available in ARGUMENTS).

---

## Step 1 — Classify with Haiku

Spawn an Agent using the Haiku model to classify the request.

Agent prompt (replace `{{REQUEST}}` with the actual ARGUMENTS value):

```
Classify this developer request into exactly one word from this list:
DEV | TESTER | SEC | REFACTOR | VALIDATE | SIMPLIFY | UNKNOWN

Routing rules:
  DEV      → full pipeline, dev cycle, end-to-end, הכל, מלא, pipeline שלם
  TESTER   → test, tests, assumptions, coverage, falsification, pytest, בדוק טסטים
  SEC      → security, אבטחה, vulnerability, vuln, injection, OWASP, path traversal
  REFACTOR → refactor, רפקטור, structure, restructure, clean up, reorganize
  VALIDATE → validate, validation, requirements, scoring, דרישות, confidence
  SIMPLIFY → simplify, פשט, simplification, dead code, quality, duplication, naming

Request: {{REQUEST}}

Reply with one word only — no explanation, no punctuation.
```

Use `model: haiku` when spawning this agent.

---

## Step 2 — Route to Workflow

Based on the single-word result from the Haiku agent:

| Result   | Invoke Skill         |
|----------|----------------------|
| DEV      | `dev-cycle`          |
| TESTER   | `test-assumptions` (if the user mentions assumptions or specific code) OR `test-generate-suite` (if the user wants full coverage) |
| SEC      | `security-review`    |
| REFACTOR | `refactor-code-structure` |
| VALIDATE | `validate-requirements-static` |
| SIMPLIFY | `simplify`           |
| UNKNOWN  | → go to Step 3       |

Pass the original ARGUMENTS along to the chosen skill as context.

---

## Step 3 — Fallback (only if UNKNOWN)

Show this routing menu and ask the user to pick:

| מה אתה רוצה? | Workflow |
|---|---|
| Pipeline מלא end-to-end | `/experts dev-cycle` |
| בדיקת assumptions / pytest suite | `/experts tester` |
| סקירת אבטחה | `/experts security-review` |
| רפקטורינג מבנה | `/experts refactor` |
| וולידציה של דרישות | `/experts validate` |
| פישוט וניקוי קוד | `/experts simplify` |

Use AskUserQuestion to let the user choose, then invoke the matching skill.
