"""
runner/run.py — GitHub Actions entrypoint for software-dev-agents.

All LLM calls go through GitHub Models (OpenAI-compatible endpoint).
GITHUB_TOKEN is the only credential needed — no ANTHROPIC_API_KEY required.

Free models used (verify availability at github.com/marketplace/models):
  gpt-4o-mini                  — OpenAI, free tier, fast
  Meta-Llama-3.1-70B-Instruct  — Meta, free tier, high quality

Agent routing by issue label:
  validate   → Agent 2 (Validator)    — Meta-Llama-3.1-70B-Instruct
  test       → Agent 3 (Testing)      — Meta-Llama-3.1-70B-Instruct
  refactor   → Agent 1 (Refactoring)  — Meta-Llama-3.1-70B-Instruct
  dev-cycle  → Agents 2→3→1 pipeline — Meta-Llama-3.1-70B-Instruct
"""

from __future__ import annotations

import os
import re
import subprocess
import sys

import yaml
from openai import OpenAI

# ── GitHub Models client ────────────────────────────────────────────────────

GITHUB_MODELS_BASE_URL = "https://models.inference.ai.azure.com"
SONNET_MODEL = "Meta-Llama-3.1-70B-Instruct"  # Free tier — high quality

_client = OpenAI(
    base_url=GITHUB_MODELS_BASE_URL,
    api_key=os.environ["GITHUB_TOKEN"],
)


def call_llm(system_prompt: str, user_message: str, model: str = SONNET_MODEL) -> str:
    response = _client.chat.completions.create(
        model=model,
        max_tokens=8192,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": user_message},
        ],
    )
    return response.choices[0].message.content


# ── Prompt loading ──────────────────────────────────────────────────────────

def load_agent_prompt(agent_num: str) -> str:
    with open("agents/prompts/prompt_versions.yaml") as f:
        versions = yaml.safe_load(f)
    version = versions["active"][f"agent_{agent_num}"]
    path = f"agents/prompts/versions/agent_{agent_num}_{version}.md"
    with open(path) as f:
        return f.read()


# ── GitHub comment ──────────────────────────────────────────────────────────

def post_comment(body: str) -> None:
    subprocess.run(
        ["gh", "issue", "comment", ISSUE_NUMBER, "--body", body, "--repo", REPO],
        check=True,
        env={**os.environ, "GH_TOKEN": os.environ["GH_TOKEN"]},
    )


# ── Routing table ───────────────────────────────────────────────────────────

# label → (agent_number, model)
ROUTES: dict[str, tuple[str, str]] = {
    "validate":  ("2", SONNET_MODEL),
    "test":      ("3", SONNET_MODEL),
    "refactor":  ("1", SONNET_MODEL),
}


def run_dev_cycle() -> str:
    """Runs agents 2 → 3 → 1 in sequence, passing results forward."""
    code_input = ISSUE_BODY

    post_comment("**Dev cycle started** — step 1/3: validating requirements...")
    validation = call_llm(load_agent_prompt("2"), f"CODE:\n{code_input}")

    # Check for FAILED/MISSING before continuing
    if re.search(r"STATUS:\s*(FAILED|MISSING)", validation, re.I):
        return f"## Validation failed — pipeline stopped\n\n{validation}"

    post_comment("**Dev cycle** — step 2/3: generating tests...")
    test_input = f"VALIDATION_REPORT:\n{validation}\n\nCODE:\n{code_input}"
    testing = call_llm(load_agent_prompt("3"), test_input)

    post_comment("**Dev cycle** — step 3/3: refactoring...")
    refactor_input = (
        f"VALIDATION_REPORT:\n{validation}\n\n"
        f"TEST_RESULTS:\n{testing}\n\n"
        f"CODE:\n{code_input}"
    )
    refactoring = call_llm(load_agent_prompt("1"), refactor_input)

    return (
        f"## Dev Cycle Complete\n\n"
        f"<details><summary>Validation report</summary>\n\n{validation}\n\n</details>\n\n"
        f"<details><summary>Test results</summary>\n\n{testing}\n\n</details>\n\n"
        f"## Refactoring result\n\n{refactoring}"
    )


# ── Main ────────────────────────────────────────────────────────────────────

LABEL = os.environ["AGENT_LABEL"]
ISSUE_BODY = os.environ.get("ISSUE_BODY", "")
ISSUE_NUMBER = os.environ["ISSUE_NUMBER"]
REPO = os.environ["GITHUB_REPOSITORY"]

try:
    if LABEL == "dev-cycle":
        result = run_dev_cycle()
    elif LABEL in ROUTES:
        agent_num, model = ROUTES[LABEL]
        result = call_llm(load_agent_prompt(agent_num), ISSUE_BODY, model)
        result = f"## Agent {agent_num} — `{LABEL}`\n\n{result}"
    else:
        post_comment(f"Unknown label `{LABEL}`. Supported: {', '.join(ROUTES)} , dev-cycle")
        sys.exit(0)

    footer = f"\n\n---\n*Model: `{SONNET_MODEL}` via GitHub Models · Label: `{LABEL}`*"
    post_comment(result + footer)

except Exception as exc:
    post_comment(f"**Agent error** (`{LABEL}`):\n```\n{exc}\n```")
    sys.exit(1)
