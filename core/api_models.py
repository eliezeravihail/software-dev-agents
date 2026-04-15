from __future__ import annotations

from pydantic import BaseModel, Field
from core.models import (
    CodeArtifact,
    Requirement,
    BooksRef,
    RefactoringOutput,
    ValidationOutput,
    TestCoverageOutput,
    RefactorMode,
    PromptVersionRef,
)


class DevelopmentTask(BaseModel):
    task_id: str
    code: CodeArtifact
    requirements: list[Requirement]
    constraints: list[str] = []
    books_refs: list[BooksRef] = []
    approval_policy: RefactorMode = RefactorMode.REVIEW


class DevelopmentResult(BaseModel):
    task_id: str
    success: bool
    validation_static: ValidationOutput | None = None
    assumption_tests: TestCoverageOutput | None = None
    validation_final: ValidationOutput | None = None
    refactoring: RefactoringOutput | None = None
    coverage: TestCoverageOutput | None = None
    prompt_versions: list[PromptVersionRef] = []
    errors: list[str] = []
    metrics: dict[str, float] = Field(default_factory=dict)
