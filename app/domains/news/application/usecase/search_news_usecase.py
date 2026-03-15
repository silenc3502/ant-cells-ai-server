from app.domains.news.application.port.news_search_port import NewsSearchPort
from app.domains.news.application.request.search_news_request import SearchNewsRequest
from app.domains.news.application.response.search_news_response import (
    NewsItemResponse,
    SearchNewsResponse,
)


class SearchNewsUseCase:
    def __init__(self, news_search_port: NewsSearchPort):
        self.news_search_port = news_search_port

    async def execute(self, request: SearchNewsRequest) -> SearchNewsResponse:
        items, total_count = await self.news_search_port.search(
            keyword=request.keyword,
            page=request.page,
            size=request.size,
        )

        return SearchNewsResponse(
            items=[
                NewsItemResponse(
                    title=item.title,
                    snippet=item.snippet,
                    source=item.source,
                    published_at=item.published_at,
                    link=item.link,
                )
                for item in items
            ],
            total_count=total_count,
            page=request.page,
            size=request.size,
        )
