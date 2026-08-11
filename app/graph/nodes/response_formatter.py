from app.graph.state import AgentState
from app.schemas.response import AnalyticsResponse
from app.config.logging import get_logger

logger = get_logger(__name__)


def response_formatter_node(state: AgentState):

    logger.info("Formatting final analytics response")


    response = AnalyticsResponse(
        question=state['question'],
        summary=state['executive_summary'],
        chart=state['chart_config'],
        result=state['query_result']
    )

    logger.info("Final analytics response created successfully")

    return {
        "final_response": response
    }