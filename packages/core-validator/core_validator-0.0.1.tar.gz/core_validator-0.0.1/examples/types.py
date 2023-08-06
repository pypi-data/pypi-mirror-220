from core_validator import ErrorSchema, ValidationContext
from pydantic import BaseModel


class CommentDto(BaseModel):
    comment: str
    post_id: int
    owner_id: int


class Source(BaseModel):
    local: str


class SourceMultiple(BaseModel):
    local: str
    position: int


class CustomValidationContext(ValidationContext[ErrorSchema[Source]]):
    is_approved: bool = False
