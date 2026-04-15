"""
agents/refactorer.py
====================
Concrete implementation of the Refactorer agent.
Demonstrates the pattern all agents follow:
  1. self.config.model is used for every LLM call
  2. Tools are injected, not instantiated here
  3. run() is the only public method
"""

from __future__ import annotations

from core.models import AgentRole, RefactoringInput, RefactoringOutput
from core.agent_config import AgentModelConfig
from agents.base_agent import BaseAgent
from agents.tool_registry import LLMCallerTool, LLMCallInput, BooksLoaderTool


SYSTEM_PROMPT = (
    "You are a senior software engineer specializing exclusively in code refactoring. "
    "Improve structure, readability, and maintainability — never change observable behavior. "
    "Always explain why each change was made. Output must follow the exact REFACTORING REPORT format."
)


class Refactorer(BaseAgent[RefactoringInput, RefactoringOutput]):

    role = AgentRole.REFACTORER

    def __init__(
        self,
        llm_tool: LLMCallerTool,
        books_tool: BooksLoaderTool,
        config: AgentModelConfig | None = None,
    ):
        super().__init__(config)
        self.llm    = llm_tool
        self.books  = books_tool

    async def run(self, input_data: RefactoringInput) -> RefactoringOutput:
        # 1. Load relevant BOOKS context (REFACTORING + any domain refs)
        books_context = await self._load_books(input_data)

        # 2. Build user message
        user_msg = self._build_prompt(input_data, books_context)

        # 3. Call LLM — model comes from self.config, never hardcoded
        llm_output = await self.llm.execute(LLMCallInput(
            system_prompt=SYSTEM_PROMPT,
            user_message=user_msg,
            model=self.config.model,            # ← injected config
            max_tokens=self.config.max_tokens,
        ))

        # 4. Parse structured output → RefactoringOutput
        return self._parse_output(input_data, llm_output.content)

    async def _load_books(self, input_data: RefactoringInput) -> str:
        parts = []
        for ref in input_data.books_refs:
            result = await self.books.execute(
                __import__("agents.tool_registry", fromlist=["BooksLoaderInput"])
                .BooksLoaderInput(
                    category=ref.category,
                    book_slug=ref.book_slug,
                    topic_file=ref.topic_file,
                )
            )
            if result.found:
                parts.append(f"## {ref.category}/{ref.topic_file}\n{result.content}")
        return "\n\n".join(parts) if parts else ""

    def _build_prompt(self, input_data: RefactoringInput, books_context: str) -> str:
        lines = [
            f"TASK ID: {input_data.task_id}",
            f"LANGUAGE: {input_data.code.language}",
        ]
        if input_data.code.framework:
            lines.append(f"FRAMEWORK: {input_data.code.framework}")
        if input_data.constraints:
            lines.append(f"CONSTRAINTS: {'; '.join(input_data.constraints)}")
        if books_context:
            lines.append(f"\n### REFERENCE MATERIAL (from BOOKS skill)\n{books_context}")
        lines.append(f"\n### CODE TO REFACTOR\n```{input_data.code.language}\n{input_data.code.content}\n```")
        return "\n".join(lines)

    def _parse_output(self, input_data: RefactoringInput, raw: str) -> RefactoringOutput:
        import re
        from core.models import (
            RefactoringChange, CodeArtifact, RefactorMode, RiskLevel, DiffImpact,
        )

        _SAFE_DEFAULTS = dict(
            refactor_mode=RefactorMode.BLOCKED,
            aggregate_confidence=0.0,
            aggregate_risk=RiskLevel.HIGH,
        )

        def _parse_refactor_mode(text: str) -> RefactorMode:
            m = re.search(r"REFACTOR_MODE\s*:\s*(auto|review|blocked)", text, re.I)
            if not m:
                return _SAFE_DEFAULTS["refactor_mode"]
            return RefactorMode(m.group(1).lower())

        def _parse_confidence(text: str) -> float:
            m = re.search(r"AGGREGATE_CONFIDENCE\s*:\s*([0-9]*\.?[0-9]+)", text, re.I)
            if not m:
                return _SAFE_DEFAULTS["aggregate_confidence"]
            return max(0.0, min(1.0, float(m.group(1))))

        def _parse_risk(text: str) -> RiskLevel:
            m = re.search(r"AGGREGATE_RISK\s*:\s*(low|medium|high)", text, re.I)
            if not m:
                return _SAFE_DEFAULTS["aggregate_risk"]
            return RiskLevel(m.group(1).lower())

        def _parse_changes(text: str) -> list[RefactoringChange]:
            changes_block = re.search(
                r"CHANGES\s*:\s*\n(.*?)(?=\nBEHAVIOR_GUARANTEE|\nREFACTORED_CODE|$)",
                text, re.S | re.I,
            )
            if not changes_block:
                return []
            changes = []
            for line in changes_block.group(1).splitlines():
                line = line.strip().lstrip("- ")
                if not line:
                    continue
                parts = [p.strip() for p in line.split("|")]
                description = parts[0] if parts else line

                pattern = None
                risk = RiskLevel.LOW
                reversible = True
                lines_added = lines_removed = 0
                api_changed = False

                for part in parts[1:]:
                    kv = part.split(":", 1)
                    if len(kv) != 2:
                        continue
                    k, v = kv[0].strip().lower(), kv[1].strip()
                    if k == "pattern":
                        pattern = v
                    elif k == "risk":
                        try:
                            risk = RiskLevel(v.lower())
                        except ValueError:
                            pass
                    elif k == "reversible":
                        reversible = v.lower() != "no"
                    elif k in ("+n/-m lines", "lines"):
                        diff_m = re.search(r"\+(\d+)/-(\d+)", v)
                        if diff_m:
                            lines_added = int(diff_m.group(1))
                            lines_removed = int(diff_m.group(2))
                    elif k == "api_changed":
                        api_changed = v.lower() == "yes"

                changes.append(RefactoringChange(
                    description=description,
                    pattern=pattern,
                    risk=risk,
                    reversible=reversible,
                    diff_impact=DiffImpact(
                        lines_added=lines_added,
                        lines_removed=lines_removed,
                        public_api_changed=api_changed,
                    ),
                ))
            return changes

        def _parse_behavior_guarantee(text: str) -> str:
            m = re.search(
                r"BEHAVIOR_GUARANTEE\s*:\s*\n(.*?)(?=\nREFACTORED_CODE|$)",
                text, re.S | re.I,
            )
            return m.group(1).strip() if m else "No behavior guarantee provided."

        def _parse_refactored_code(text: str, language: str) -> str:
            m = re.search(
                r"REFACTORED_CODE\s*:\s*\n```[^\n]*\n(.*?)```",
                text, re.S | re.I,
            )
            return m.group(1) if m else text

        refactor_mode = _parse_refactor_mode(raw)
        aggregate_confidence = _parse_confidence(raw)
        aggregate_risk = _parse_risk(raw)
        changes = _parse_changes(raw)
        behavior_guarantee = _parse_behavior_guarantee(raw)
        code_content = _parse_refactored_code(raw, input_data.code.language)

        return RefactoringOutput(
            task_id=input_data.task_id,
            original_code=input_data.code,
            refactored_code=CodeArtifact(
                language=input_data.code.language,
                framework=input_data.code.framework,
                content=code_content,
            ),
            changes=changes,
            behavior_guarantee=behavior_guarantee,
            aggregate_risk=aggregate_risk,
            aggregate_confidence=aggregate_confidence,
            refactor_mode=refactor_mode,
        )
