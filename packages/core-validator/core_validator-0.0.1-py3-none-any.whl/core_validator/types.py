import dataclasses
from enum import Enum
from collections.abc import Callable, Coroutine, Sequence
from typing import Any, Generic, TypeAlias, TypeVar


_T = TypeVar("_T")
_S = TypeVar("_S")

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


class ValidationError(Generic[_T], Exception):
    messages: list[_T]

    def __init__(self, messages: list[_T], *args: object) -> None:
        super().__init__(*args)
        self.messages = messages


@dataclasses.dataclass(frozen=True, slots=True)
class ValidationContext(Generic[_T]):
    _errors: list[_T] = dataclasses.field(default_factory=list)

    def add_error(self, error: _T) -> None:
        if error not in self._errors:
            self._errors.append(error)

    def extend_error(self, errors: Sequence[_T]) -> None:
        self._errors.extend(errors)

    @property
    def errors(self) -> list[_T]:
        return self._errors
