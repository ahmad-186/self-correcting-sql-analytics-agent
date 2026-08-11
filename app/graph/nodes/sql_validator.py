from app.graph.state import AgentState
from app.tools.sql_validator import validate_sql
from app.schemas.validation import SQLValidationResult
from app.config.logging import get_logger

logger = get_logger(__name__)

def sql_validator_node(state: AgentState):
    """
    Validate the generated SQL before execution.
    """

    generated_sql = state["generated_sql"]
    database_schema = state["database_schema"]

    logger.info("SQL validation started")

    if generated_sql is None:
        logger.warning(
            "SQL validation skipped because SQL generation failed"
        )

        return {
            "validation_result": SQLValidationResult(
                is_valid=False,
                failed_Check=None,
                error_message=state["error_message"]
            )
        }

    validation_result = validate_sql(
        generated_sql,
        database_schema
    )

    if validation_result.is_valid:
        logger.info("SQL validation passed")
    else:
        logger.warning(
            "SQL validation failed. Check: %s | Error: %s",
            validation_result.failed_Check,
            validation_result.error_message
        )

    return {
        "validation_result": validation_result
    }