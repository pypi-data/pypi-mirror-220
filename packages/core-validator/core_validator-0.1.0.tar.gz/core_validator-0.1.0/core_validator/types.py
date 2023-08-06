import dataclasses
from enum import Enum
from collections.abc import Callable, Coroutine, Sequence
from typing import Any, Generic, TypeAlias, TypeVar


TError = TypeVar("TError")
_S = TypeVar("_S")

TValidationData = TypeVar("TValidationData")

SelfValidator: TypeAlias = Any  # heh

ValidatorFunc: TypeAlias = Callable[[Any], Coroutine[Any, Any, None] | None]


class ErrorCodeEnum(str, Enum):
    unique_constraint = "UNIQUE CONSTRAINT"
    not_found = "NOT FOUND"
    permission_denied = "PERMISSION DENIED"


@dataclasses.dataclass
class ErrorSchema(Generic[_S]):
    code: str
    message: str
    detail: str | None = None
    source: _S | None = None


class ValidationError(Generic[TError], Exception):
    messages: list[TError]

    def __init__(self, messages: list[TError], *args: object) -> None:
        super().__init__(*args)
        self.messages = messages


@dataclasses.dataclass(frozen=True, slots=True)
class ValidationContext(Generic[TError]):
    _errors: list[TError] = dataclasses.field(default_factory=list, init=False)

    def add_error(self, error: TError) -> None:
        if error not in self._errors:
            self._errors.append(error)

    def extend_error(self, errors: Sequence[TError]) -> None:
        self._errors.extend(errors)

    @property
    def errors(self) -> list[TError]:
        return self._errors
