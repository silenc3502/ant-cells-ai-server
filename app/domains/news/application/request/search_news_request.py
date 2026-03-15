from pydantic import BaseModel, field_validator


class SearchNewsRequest(BaseModel):
    keyword: str
    page: int = 1
    size: int = 10

    @field_validator("keyword")
    @classmethod
    def keyword_must_not_be_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("keyword must not be empty")
        return v.strip()

    @field_validator("page")
    @classmethod
    def page_must_be_positive(cls, v: int) -> int:
        if v < 1:
            raise ValueError("page must be at least 1")
        return v

    @field_validator("size")
    @classmethod
    def size_must_be_valid(cls, v: int) -> int:
        if v < 1 or v > 100:
            raise ValueError("size must be between 1 and 100")
        return v
