import pytest
from examples.types import CommentDto
from tests.factories import CommentFactory


@pytest.fixture(autouse=True)
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture
def random_body() -> list[CommentDto]:
    return [CommentFactory(owner_id=-5) for _ in range(100)]
