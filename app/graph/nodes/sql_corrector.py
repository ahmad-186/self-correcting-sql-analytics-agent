from app.graph.state import AgentState
from app.models.sql_corrector import corrected_sql
from app.prompts.sql_corrector import build_corrected_sql_prompt
from app.config.logging import get_logger

logger = get_logger(__name__)


def sql_corrector_node(state: AgentState):

    question = state["question"]
    schema_context = state["schema_context"]
    generated_sql = state["generated_sql"]
    validation_result = state["validation_result"]

    retry_count = state["retry_count"] + 1

    logger.info(
        "SQL correction started. Retry attempt: %d",
        retry_count
    )

    prompt = build_corrected_sql_prompt(
        question=question,
        schema_context=schema_context,
        generated_sql=generated_sql,
        validation_error=validation_result
    )

    result = corrected_sql(prompt)

    if not result.success:
        logger.warning(
            "SQL correction failed on retry attempt %d: %s",
            retry_count,
            result.reason
        )
    else:
        logger.info(
            "SQL correction completed successfully on retry attempt %d",
            retry_count
        )

    return {
        "generated_sql": result.sql,
        "error_message": result.reason,
        "retry_count": retry_count
    }