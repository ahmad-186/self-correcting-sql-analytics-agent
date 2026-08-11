from app.graph.state import AgentState
from app.tools.sql_executor import execute_sql
from app.config.logging import get_logger

logger = get_logger(__name__)


def sql_executor_node(state: AgentState):
    """
    Execute the validated SQL query.
    """

    generated_sql = state["generated_sql"]

    logger.info("SQL execution started")

    query_result = execute_sql(generated_sql)

    logger.info(
        "SQL execution completed. Rows returned: %d",
        len(query_result)
    )

    return {
        "query_result": query_result
    }