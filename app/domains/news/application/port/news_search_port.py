from abc import ABC, abstractmethod
from typing import Tuple, List

from app.domains.news.domain.entity.news_item import NewsItem


class NewsSearchPort(ABC):
    @abstractmethod
    async def search(self, keyword: str, page: int, size: int) -> Tuple[List[NewsItem], int]:
        pass
