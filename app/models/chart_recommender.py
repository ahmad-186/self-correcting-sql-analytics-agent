from app.models.client import llm
from app.schemas.chart_config import ChartRecommendation
from app.prompts.chart_recommender import build_chart_prompt

structured_llm = llm.with_structured_output(ChartRecommendation)

def recommended_chart(question: str, analysis) -> ChartRecommendation:
    """
    Use the LLM to recommend the visualization.
    """

    prompt = build_chart_prompt(question=question, analysis=analysis)

    response = structured_llm.invoke(prompt)

    return response