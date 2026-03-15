from dataclasses import dataclass
from typing import Optional


@dataclass
class NewsItem:
    title: str
    snippet: str
    source: str
    published_at: str
    link: Optional[str] = None
