from langgraph.graph import END
from app.config.settings import settings

def route_after_validation(state):
    """
    Decide the next step after SQL validation.
    """

    validation_result = state["validation_result"]

    if validation_result.is_valid:
        return "sql_executor"

    if state["retry_count"] >= settings.max_retries:
        return END
    
    if state["generated_sql"] is None:
        return END

    return "sql_corrector"