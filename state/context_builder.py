from __future__ import annotations

from core.models import RefactoringInput, ValidationInput, TestCoverageInput
from state.workflow_state import WorkflowState


class ContextBuilder:
    @staticmethod
    def for_validation_static(state: WorkflowState) -> ValidationInput:
        return ValidationInput(
            task_id=state.task.task_id,
            code=state.task.code,
            requirements=state.task.requirements,
            books_refs=state.task.books_refs,
            phase='static',
        )

    @staticmethod
    def for_test_assumptions(state: WorkflowState) -> TestCoverageInput:
        requests = [v.test_request for v in state.static_validation.validations if v.test_request]
        return TestCoverageInput(
            task_id=state.task.task_id,
            mode='validation',
            code=state.task.code,
            test_requests=requests,
            books_refs=state.task.books_refs,
        )

    @staticmethod
    def for_validation_final(state: WorkflowState) -> ValidationInput:
        return ValidationInput(
            task_id=state.task.task_id,
            code=state.task.code,
            requirements=state.task.requirements,
            books_refs=state.task.books_refs,
            phase='final',
            test_results=state.assumption_tests.test_results if state.assumption_tests else [],
        )

    @staticmethod
    def for_refactoring(state: WorkflowState) -> RefactoringInput:
        return RefactoringInput(
            task_id=state.task.task_id,
            code=state.task.code,
            constraints=state.task.constraints,
            books_refs=state.task.books_refs,
            approval_required=state.task.approval_policy.value != 'auto',
        )

    @staticmethod
    def for_coverage(state: WorkflowState) -> TestCoverageInput:
        code = state.refactoring.refactored_code if state.refactoring else state.task.code
        return TestCoverageInput(
            task_id=state.task.task_id,
            mode='coverage',
            code=code,
            requirements=state.task.requirements,
            books_refs=state.task.books_refs,
        )
