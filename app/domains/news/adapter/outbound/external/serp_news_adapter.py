from typing import Tuple, List

import httpx

from app.domains.news.application.port.news_search_port import NewsSearchPort
from app.domains.news.domain.entity.news_item import NewsItem


class SerpNewsAdapter(NewsSearchPort):
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://serpapi.com/search"

    async def search(self, keyword: str, page: int, size: int) -> Tuple[List[NewsItem], int]:
        start = (page - 1) * size

        params = {
            "engine": "google_news",
            "q": keyword,
            "api_key": self.api_key,
            "start": start,
            "num": size,
        }

        async with httpx.AsyncClient() as client:
            response = await client.get(self.base_url, params=params, timeout=10.0)
            response.raise_for_status()
            data = response.json()

        news_results = data.get("news_results", [])
        total_count = data.get("search_information", {}).get("total_results", len(news_results))

        items = [
            NewsItem(
                title=result.get("title", ""),
                snippet=result.get("snippet", ""),
                source=result.get("source", {}).get("name", "") if isinstance(result.get("source"), dict) else result.get("source", ""),
                published_at=result.get("date", ""),
                link=result.get("link"),
            )
            for result in news_results
        ]

        return items, total_count
