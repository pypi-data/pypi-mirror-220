import pytest
from examples.types import CommentDto
from examples.single_error import CommentValidator


pytestmark = [pytest.mark.anyio]


async def test_random_data(random_body: list[CommentDto]) -> None:
    for comment in random_body:
        validator = CommentValidator(comment)
        post_in_db = 1 <= comment.post_id < 10
        owner_in_db = 1 <= comment.owner_id < 10

        errors = await validator.errors()
        if not post_in_db:
            assert any(
                [
                    error.source is not None and error.source.local == "data/post_id"
                    for error in errors
                ]
            )

        if not owner_in_db:
            assert any(
                [
                    error.source is not None and error.source.local == "data/owner_id"
                    for error in errors
                ]
            )
