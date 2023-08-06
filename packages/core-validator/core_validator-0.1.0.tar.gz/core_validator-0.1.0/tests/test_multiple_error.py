import pytest
from examples.types import CommentDto
from examples.multiple_error import CommentValidator


pytestmark = [pytest.mark.anyio]


async def test_random_data(random_body: list[CommentDto]) -> None:
    validator = CommentValidator()
    assert len(await validator.errors(random_body)) > 0
