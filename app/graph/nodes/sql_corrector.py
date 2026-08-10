from app.graph.state import AgentState
from app.models.sql_corrector import corrected_sql
from app.prompts.sql_corrector import build_corrected_sql_prompt

def sql_corrector_node(state: AgentState):

    question = state["question"]
    schema_context = state["schema_context"]
    generated_sql = state["generated_sql"]
    validation_result = state["validation_result"]

    prompt = build_corrected_sql_prompt(
        question=question, 
        schema_context=schema_context, 
        generated_sql=generated_sql, 
        validation_error=validation_result
        )


    result = corrected_sql(prompt)

    return {
        "generated_sql": result.sql,
        "error_message": result.reason,
        "retry_count" : state["retry_count"] + 1
    }