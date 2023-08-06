import asyncio
import dataclasses
import functools
from core_validator import (
    ValidationError,
    ErrorSchema,
    ErrorCodeEnum,
    validate,
)
from core_validator import Validator
from examples.types import CommentDto, CustomValidationContext, SourceMultiple


@dataclasses.dataclass()
class CommentValidator(Validator[list[CommentDto], ErrorSchema[SourceMultiple]]):
    @functools.cached_property
    def context(self) -> CustomValidationContext:  # type: ignore[override]
        return CustomValidationContext()

    @validate
    async def test1(self):
        post_ids = range(1, 10)
        for i, dto in enumerate(self.data):
            if dto.post_id not in post_ids:
                self.context.add_error(
                    ErrorSchema(
                        code=ErrorCodeEnum.not_found.value,
                        message="Id doen't not exists",
                        detail=f"Post with id={dto.post_id} not found",
                        source=SourceMultiple(
                            local="data/post_id",
                            position=i,
                        ),
                    )
                )

    @validate
    async def test2(self):
        owner_ids = range(1, 10)
        for i, dto in enumerate(self.data):
            if dto.owner_id not in owner_ids:
                self.context.add_error(
                    ErrorSchema(
                        code=ErrorCodeEnum.not_found.value,
                        message="Id doen't not exists",
                        detail=f"User with id={dto.post_id} not found",
                        source=SourceMultiple(
                            local="data/owner_id",
                            position=i,
                        ),
                    )
                )


async def main():
    dto_list = [
        CommentDto(comment="comment", owner_id=1, post_id=1),
        CommentDto(comment="comment", owner_id=1, post_id=100),
        CommentDto(comment="comment", owner_id=100, post_id=1),
        CommentDto(comment="comment", owner_id=1234, post_id=1234),
    ]
    try:
        await CommentValidator().validate(dto_list)
    except ValidationError as e:
        for message in e.messages:
            print(message)


if __name__ == "__main__":
    asyncio.run(main())
