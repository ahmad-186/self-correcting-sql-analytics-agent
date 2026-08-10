from app.models.client import llm
from app.schemas.sql import SQLGenerationResult

structured_llm = llm.with_structured_output(SQLGenerationResult)

def generate_sql(prompt: str) -> SQLGenerationResult:
    """
    Generate SQL using the configured LLM.
    """

    response = structured_llm.invoke(prompt)

    return response