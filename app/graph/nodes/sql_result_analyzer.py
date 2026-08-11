from app.graph.state import AgentState
from app.tools.result_analyzer import analyze_result
from app.config.logging import get_logger

logger = get_logger(__name__)

def result_analyzer_node(state: AgentState):

    query_result = state["query_result"]

    logger.info("Result analysis started")

    analysis = analyze_result(query_result)

    logger.info(
        "Result analysis completed. Rows: %d | Numeric: %d | "
        "Categorical: %d | Datetime: %d",
        analysis.row_count,
        len(analysis.numeric_columns),
        len(analysis.categorical_columns),
        len(analysis.datetime_columns),
    )
    
    return {
        "result_analysis": analysis
    }