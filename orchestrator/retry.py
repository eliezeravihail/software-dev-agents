from __future__ import annotations

import asyncio
from dataclasses import dataclass
from typing import Awaitable, Callable, TypeVar

T = TypeVar('T')


@dataclass(frozen=True)
class RetryPolicy:
    max_attempts: int
    base_delay: float
    max_delay: float


class AdaptiveRetryPlanner:
    def strategy_hint(self, attempt: int, previous_error: str | None) -> str:
        if attempt <= 1:
            return 'standard'
        if attempt == 2:
            return f'focus_on_previous_failure: {previous_error or "unknown"}'
        return 'simplify_scope_and_return_structured_output_only'


async def execute_with_retry(
    func: Callable[[str], Awaitable[T]],
    policy: RetryPolicy,
    retryable: tuple[type[BaseException], ...] = (TimeoutError, ConnectionError),
) -> T:
    planner = AdaptiveRetryPlanner()
    previous_error = None
    for attempt in range(1, policy.max_attempts + 1):
        try:
            return await func(planner.strategy_hint(attempt, previous_error))
        except retryable as exc:
            previous_error = str(exc)
            if attempt >= policy.max_attempts:
                raise
            delay = min(policy.base_delay * (2 ** (attempt - 1)), policy.max_delay)
            await asyncio.sleep(delay)
