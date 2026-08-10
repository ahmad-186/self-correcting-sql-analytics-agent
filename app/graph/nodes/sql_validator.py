from app.graph.state import AgentState
from app.tools.sql_validator import validate_sql
from app.schemas.validation import SQLValidationResult

def sql_validator_node(state: AgentState):
    """
    Validate the generated SQL before Execution.
    """

    generated_sql = state["generated_sql"]
    database_schema = state["database_schema"]

    if generated_sql is None:
        return {
            "validation_result": SQLValidationResult(
                is_valid=False,
                failed_Check=None,
                error_message=state["error_message"]
            )
        }

    validation_result = validate_sql(generated_sql, database_schema)

    return {"validation_result": validation_result}