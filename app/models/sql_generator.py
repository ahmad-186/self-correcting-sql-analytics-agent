from app.models.client import llm
from app.schemas.sql import SQLGenerationResult
from app.config.logging import get_logger

logger = get_logger(__name__)

structured_llm = llm.with_structured_output(SQLGenerationResult)

def generate_sql(prompt: str) -> SQLGenerationResult:
    """
    Generate SQL using the configured LLM.
    """

    logger.info("Calling LLM for SQL generation")

    response = structured_llm.invoke(prompt)

    logger.info("LLM SQL generation response received")

    return response