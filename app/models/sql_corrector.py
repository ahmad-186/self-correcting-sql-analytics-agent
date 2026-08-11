from app.models.client import llm
from app.schemas.sql import SQLGenerationResult
from app.config.logging import get_logger

logger = get_logger(__name__)

structured_llm = llm.with_structured_output(SQLGenerationResult)


def corrected_sql(prompt: str) -> SQLGenerationResult:
    """
    Correct an invalid SQL query using the validation error.
    """

    logger.info("Calling LLM for SQL correction")

    response = structured_llm.invoke(prompt)

    logger.info("LLM SQL correction response received")

    return response