from app.models.client import llm
from app.schemas.sql import SQLGenerationResult

structured_llm = llm.with_structured_output(SQLGenerationResult)

def corrected_sql(prompt: str) -> SQLGenerationResult:
    """
    Correct an Invalid SQL query using the validation error.
    """

    response = structured_llm.invoke(prompt)

    return response