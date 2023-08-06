from factory import Factory, Faker

from examples.types import CommentDto


class CommentFactory(Factory):
    class Meta:
        model = CommentDto

    comment = Faker("pystr")
    post_id = Faker("pyint")
    owner_id = Faker("pyint")
