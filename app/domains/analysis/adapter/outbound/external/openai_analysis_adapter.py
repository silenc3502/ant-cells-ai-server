import json
import logging

import httpx

from app.domains.analysis.application.port.article_analysis_port import ArticleAnalysisPort
from app.domains.analysis.domain.entity.analysis_result import AnalysisResult

logger = logging.getLogger(__name__)


class OpenAIAnalysisAdapter(ArticleAnalysisPort):
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.openai.com/v1/responses"

    async def analyze(self, content: str) -> AnalysisResult:
        if not self.api_key or not self.api_key.strip():
            logger.error("[OpenAI] API 키가 비어 있습니다!")
            raise ValueError("OPENAI_API_KEY가 설정되지 않았습니다")

        logger.info("[OpenAI] API 키 확인됨 (앞 8자: %s...)", self.api_key[:8])
        logger.info("[OpenAI] 분석 요청 content 길이: %d자", len(content))

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": "gpt-5-mini",
            "instructions": (
                "You are an article analysis assistant. "
                "Analyze the given article and return a JSON object with the following fields:\n"
                '- "keywords": a list of up to 5 key keywords (strings) from the article\n'
                '- "sentiment": one of "positive", "negative", or "neutral"\n'
                '- "sentiment_score": a float between -1.0 (most negative) and 1.0 (most positive)\n'
                "Return ONLY the JSON object, no other text."
            ),
            "input": content,
        }

        logger.info("[OpenAI] 요청 전송 중... (model=%s, url=%s)", payload["model"], self.base_url)

        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.base_url,
                headers=headers,
                json=payload,
                timeout=30.0,
            )
            logger.info("[OpenAI] 응답 상태 코드: %d", response.status_code)

            if response.status_code != 200:
                logger.error("[OpenAI] 요청 실패! 상태: %d, 응답 본문: %s",
                             response.status_code, response.text)
                response.raise_for_status()

            data = response.json()

        raw = self._extract_output_text(data)
        logger.info("[OpenAI] 응답 원문: %s", raw)
        parsed = json.loads(raw)
        logger.info("[OpenAI] 파싱 완료: keywords=%s, sentiment=%s, score=%s",
                     parsed.get("keywords"), parsed.get("sentiment"), parsed.get("sentiment_score"))

        return AnalysisResult(
            keywords=parsed["keywords"],
            sentiment=parsed["sentiment"],
            sentiment_score=float(parsed["sentiment_score"]),
        )

    @staticmethod
    def _extract_output_text(data: dict) -> str:
        output_text = data.get("output_text")
        if isinstance(output_text, str) and output_text.strip():
            return output_text.strip()

        parts: list[str] = []
        for item in data.get("output", []):
            if not isinstance(item, dict):
                continue
            for block in item.get("content", []):
                if not isinstance(block, dict):
                    continue
                text = block.get("text")
                if isinstance(text, str) and text.strip():
                    parts.append(text.strip())

        result = "\n".join(parts).strip()
        if not result:
            raise ValueError("OpenAI Responses API에서 텍스트 출력을 찾을 수 없습니다")
        return result
