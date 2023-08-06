import asyncio
import dataclasses
from core_validator import (
    ValidationError,
    ErrorSchema,
    ErrorCodeEnum,
    validate,
    pre_state,
)
from core_validator import Validator
from examples.types import CommentDto, Source


negative_id_error = ErrorSchema(
    code=ErrorCodeEnum.not_found.value,
    message="Id < 0",
    detail="Id must > 0",
    source=Source(
        local="data/owner_id",
    ),
)


@dataclasses.dataclass()
class CommentValidator(Validator[CommentDto, ErrorSchema[Source]]):
    @validate
    async def test1(self):
        post_ids = list(range(1, 10))
        if self.data.post_id not in post_ids:
            self.context.add_error(
                ErrorSchema(
                    code=ErrorCodeEnum.not_found.value,
                    message="Id doen't not exists",
                    detail=f"Post with id={self.data.post_id} not found",
                    source=Source(
                        local="data/post_id",
                    ),
                )
            )

    @validate
    @pre_state(lambda self: self.data.owner_id > 0, negative_id_error)
    async def test2(self):
        owner_ids = list(range(1, 10))

        if self.data.owner_id not in owner_ids:
            self.context.add_error(
                ErrorSchema(
                    code=ErrorCodeEnum.not_found.value,
                    message="Id doen't not exists",
                    detail=f"User with id={self.data.post_id} not found",
                    source=Source(
                        local="data/owner_id",
                    ),
                )
            )


async def main():
    dto = CommentDto(comment="comment", owner_id=1234, post_id=222)

    try:
        await CommentValidator().validate(dto)
    except ValidationError as e:
        print(e.messages)


if __name__ == "__main__":
    asyncio.run(main())
