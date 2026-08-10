from app.graph.state import AgentState
from app.prompts.sql_generator import build_sql_prompt
from app.models.sql_generator import generate_sql

def sql_generator_node(state: AgentState):

    """
    Generate SQL from the user's question
    and retrieved Schema Context.
    """

    question = state['question']
    schema_context = state['schema_context']

    prompt = build_sql_prompt(question=question, schema_context=schema_context)

    result = generate_sql(prompt)

    if not result.success:
        return {
            "generated_sql": None,
            "error_message": result.reason
        }

    return {'generated_sql': result.sql}