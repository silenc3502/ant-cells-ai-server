from fastapi import APIRouter, Query

from app.domains.news.adapter.outbound.external.serp_news_adapter import SerpNewsAdapter
from app.domains.news.application.request.search_news_request import SearchNewsRequest
from app.domains.news.application.response.search_news_response import SearchNewsResponse
from app.domains.news.application.usecase.search_news_usecase import SearchNewsUseCase
from app.infrastructure.config import get_settings

router = APIRouter(prefix="/news", tags=["news"])


@router.get("/search", response_model=SearchNewsResponse)
async def search_news(
    keyword: str = Query(..., min_length=1),
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
):
    settings = get_settings()
    adapter = SerpNewsAdapter(api_key=settings.SERP_API_KEY)
    usecase = SearchNewsUseCase(news_search_port=adapter)

    request = SearchNewsRequest(keyword=keyword, page=page, size=size)
    return await usecase.execute(request)
