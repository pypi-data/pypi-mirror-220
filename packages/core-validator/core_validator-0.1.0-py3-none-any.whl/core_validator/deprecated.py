from __future__ import annotations
from collections.abc import Sequence
from core_validator.types import (
    ValidationError,
    TError,
)
from core_validator.validator import ValidatorBase


class Validator(ValidatorBase[TError]):
    async def validate(self) -> None:
        await self.setup()
        try:
            await self._run_validate_process()
        finally:
            await self.dispose()

        if self.context.errors:
            raise ValidationError(self.context.errors)

    async def errors(self) -> Sequence[TError]:
        try:
            await self.validate()
        except ValidationError as e:
            return e.messages
        return []
