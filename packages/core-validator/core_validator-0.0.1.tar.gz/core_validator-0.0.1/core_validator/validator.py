from __future__ import annotations
import dataclasses
import functools
from collections.abc import Callable, Sequence
from typing import Any, Coroutine, Generic, Literal
from core_validator.types import (
    ValidationContext,
    ValidationError,
    ValidatorFunc,
    _T,
    SelfValidator,
)
from core_validator.utils import await_maybe


def callable_true(x: SelfValidator) -> bool:
    return True


@dataclasses.dataclass(frozen=True, slots=True)
class ValidatingFunction(Generic[_T]):
    validator_function: ValidatorFunc

    __is_validator__: Literal[True] = True
    __pre_condition__: Callable[
        [SelfValidator],
        Coroutine[Any, Any, bool] | bool,
    ] = callable_true
    __pre_state_error__: _T | None = None

    async def __call__(self, validator: Validator[_T]) -> None:
        await await_maybe(self.validator_function(validator))


def validate(
    f: ValidatorFunc | ValidatingFunction[_T],
) -> ValidatingFunction[_T]:
    if isinstance(f, ValidatingFunction):
        return ValidatingFunction(
            f.validator_function,
            __pre_condition__=f.__pre_condition__,
            __pre_state_error__=f.__pre_state_error__,
        )
    return ValidatingFunction(f)


def pre_state(
    function: Callable[
        [SelfValidator],
        Coroutine[Any, Any, bool] | bool,
    ],
    error: _T | None = None,
) -> Callable[[ValidatorFunc], ValidatorFunc]:
    def decorator(f: ValidatorFunc | ValidatingFunction[_T]) -> ValidatingFunction[_T]:
        if isinstance(f, ValidatingFunction):
            raise NotImplementedError
        return ValidatingFunction(
            validator_function=f,
            __pre_condition__=function,
            __pre_state_error__=error,
        )

    return decorator


class Validator(Generic[_T]):
    async def setup(self) -> None:
        ...

    async def dispose(self) -> None:
        ...

    async def validate(self) -> None:
        await self.setup()
        try:
            await self._run_validate_process()
        finally:
            await self.dispose()

        if self.context.errors:
            raise ValidationError(self.context.errors)

    @functools.cached_property
    def context(self) -> ValidationContext[_T]:
        return ValidationContext()

    async def errors(self) -> Sequence[_T]:
        try:
            await self.validate()
        except ValidationError as e:
            return e.messages
        return []

    async def _run_validate_process(self):
        queue = list(self._get_validation_methods())
        failed_pre_state_validators = []
        while queue:
            for validator in queue:
                if await await_maybe(validator.__pre_condition__(self)):
                    await await_maybe(validator(self))
                else:
                    failed_pre_state_validators.append(validator)

            if len(failed_pre_state_validators) == len(queue):
                break

            queue = failed_pre_state_validators.copy()
            failed_pre_state_validators = []

        for validator in failed_pre_state_validators:
            if validator.__pre_state_error__ is not None:
                self.context.add_error(validator.__pre_state_error__)

    @classmethod
    def _get_validation_methods(
        cls,
    ) -> Sequence[ValidatingFunction[_T]]:
        return [
            function
            for value in dir(cls)
            if isinstance(
                function := getattr(cls, value),
                ValidatingFunction,
            )
        ]
