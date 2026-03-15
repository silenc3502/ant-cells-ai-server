from typing import List, Optional

from pydantic import BaseModel


class NewsItemResponse(BaseModel):
    title: str
    snippet: str
    source: str
    published_at: str
    link: Optional[str] = None


class SearchNewsResponse(BaseModel):
    items: List[NewsItemResponse]
    total_count: int
    page: int
    size: int
