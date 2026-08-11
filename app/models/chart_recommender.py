from app.models.client import llm
from app.schemas.chart_config import ChartRecommendation
from app.prompts.chart_recommender import build_chart_prompt
from app.config.logging import get_logger

logger = get_logger(__name__)

structured_llm = llm.with_structured_output(ChartRecommendation)

def recommended_chart(question: str, analysis) -> ChartRecommendation:
    """
    Use the LLM to recommend the visualization.
    """

    logger.info("Calling LLM for chart recommendation")

    prompt = build_chart_prompt(question=question, analysis=analysis)

    response = structured_llm.invoke(prompt)

    logger.info(
        "LLM chart recommendation received: %s",
        response.chart_type
    )

    return response