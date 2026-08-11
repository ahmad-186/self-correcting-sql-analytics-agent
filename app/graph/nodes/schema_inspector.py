from app.graph.state import AgentState
from app.tools.schema_inspector import inspect_schema
from app.config.logging import get_logger

logger = get_logger(__name__)


def schema_inspector_node(state: AgentState):
    """
    Retrieve the relevant database schema and update the graph state
    """

    question = state["question"]

    logger.info("Schema inspection started")

    schema = inspect_schema(question)

    logger.info(
        "Schema inspection completed. Relevant schema context generated."
    )
    
    return { "schema_context": schema["schema_context"], "database_schema": schema["database_schema"]}