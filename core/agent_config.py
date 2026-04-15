from __future__ import annotations

from pydantic import BaseModel
from core.models import AgentRole


class AgentModelConfig(BaseModel):
    model: str
    max_tokens: int
    temperature: float
    prompt_version: str
    rationale: str


MODEL_REGISTRY: dict[AgentRole, AgentModelConfig] = {
    AgentRole.REFACTORING: AgentModelConfig(
        model='claude-sonnet-4-6',
        max_tokens=8192,
        temperature=0.1,
        prompt_version='v1.2',
        rationale='Deep structural code transformations with guardrails.',
    ),
    AgentRole.VALIDATOR: AgentModelConfig(
        model='claude-sonnet-4-6',
        max_tokens=6144,
        temperature=0.0,
        prompt_version='v1.2',
        rationale='Deterministic validation with confidence and risk scoring.',
    ),
    AgentRole.TESTING: AgentModelConfig(
        model='claude-sonnet-4-6',
        max_tokens=8192,
        temperature=0.1,
        prompt_version='v1.1',
        rationale='Targeted assumption tests and coverage generation.',
    ),
}


def get_config(role: AgentRole) -> AgentModelConfig:
    return MODEL_REGISTRY[role]
