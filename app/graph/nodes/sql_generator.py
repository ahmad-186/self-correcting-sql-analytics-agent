from app.graph.state import AgentState
from app.prompts.sql_generator import build_sql_prompt
from app.models.sql_generator import generate_sql
from app.config.logging import get_logger

logger = get_logger(__name__)

def sql_generator_node(state: AgentState):

    """
    Generate SQL from the user's question
    and retrieved Schema Context.
    """

    question = state['question']
    schema_context = state['schema_context']

    logger.info("SQL generation started")

    prompt = build_sql_prompt(question=question, schema_context=schema_context)

    result = generate_sql(prompt)

    if not result.success:
        logger.warning(
            "SQL generation failed: %s",
            result.reason
        )

        return {
            "generated_sql": None,
            "error_message": result.reason
        }

    logger.info("SQL generation completed successfully")

    return {'generated_sql': result.sql}