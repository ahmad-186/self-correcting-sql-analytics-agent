from app.graph.state import AgentState
from app.models.chart_recommender import recommended_chart
from app.schemas.chart_config import ChartConfig
from app.config.logging import get_logger

logger = get_logger(__name__)

def visualization_node(state: AgentState):

    analysis = state["result_analysis"]
    question = state["question"]
    query_result = state["query_result"]

    logger.info("Visualization recommendation started")

    recommendation = recommended_chart(question=question, analysis=analysis)

    logger.info(
        "Chart recommendation received: type=%s | x_axis=%s | y_axis=%s",
        recommendation.chart_type,
        recommendation.x_axis,
        recommendation.y_axis,
    )

    chart_config =  ChartConfig(
        chart_type=recommendation.chart_type,
        title=recommendation.title,
        x_axis=recommendation.x_axis,
        y_axis=recommendation.y_axis,
        data = query_result
    )

    logger.info(
        "Chart configuration created successfully: %s",
        chart_config.chart_type
    )

    return {"chart_config": chart_config}