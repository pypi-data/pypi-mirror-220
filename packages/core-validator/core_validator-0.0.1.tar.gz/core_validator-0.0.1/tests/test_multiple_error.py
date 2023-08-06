import pytest
from examples.types import CommentDto
from examples.multiple_error import CommentValidator


pytestmark = [pytest.mark.anyio]


async def test_random_data(random_body: list[CommentDto]) -> None:
    validator = CommentValidator(random_body)
    assert len(await validator.errors()) > 0
