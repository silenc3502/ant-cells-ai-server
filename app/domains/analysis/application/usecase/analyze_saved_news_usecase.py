import logging

from app.domains.analysis.application.port.article_analysis_port import ArticleAnalysisPort
from app.domains.analysis.application.response.analyze_article_response import AnalyzeArticleResponse
from app.domains.news.application.port.saved_news_repository_port import SavedNewsRepositoryPort

logger = logging.getLogger(__name__)


class AnalyzeSavedNewsUseCase:
    def __init__(
        self,
        saved_news_repository: SavedNewsRepositoryPort,
        article_analysis_port: ArticleAnalysisPort,
    ):
        self.saved_news_repository = saved_news_repository
        self.article_analysis_port = article_analysis_port

    async def execute(self, news_id: str) -> AnalyzeArticleResponse:
        logger.info("[UseCase] 기사 분석 시작 (news_id=%s)", news_id)

        saved_news = await self.saved_news_repository.find_by_id(news_id)
        if saved_news is None:
            logger.warning("[UseCase] 기사를 찾을 수 없음 (news_id=%s)", news_id)
            raise ValueError(f"저장된 기사를 찾을 수 없습니다: {news_id}")

        logger.info("[UseCase] 기사 조회 성공 (title=%s)", saved_news.title)
        logger.info("[UseCase] content 존재 여부: %s, content 길이: %d",
                     saved_news.content is not None, len(saved_news.content) if saved_news.content else 0)

        if not saved_news.content or not saved_news.content.strip():
            logger.warning("[UseCase] 기사 본문이 비어 있음 (news_id=%s)", news_id)
            raise ValueError("기사 본문이 비어 있어 분석할 수 없습니다")

        result = await self.article_analysis_port.analyze(content=saved_news.content)
        logger.info("[UseCase] 분석 완료 (keywords=%s, sentiment=%s)", result.keywords, result.sentiment)

        return AnalyzeArticleResponse(
            keywords=result.keywords,
            sentiment=result.sentiment,
            sentiment_score=result.sentiment_score,
        )
