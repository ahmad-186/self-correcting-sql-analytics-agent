from pydantic import BaseModel, Field

class SQLGenerationResult(BaseModel):
    """
    Structured output returned by the SQL generation LLM.
    """
    success: bool
    sql: str | None = Field(default=None, description="The generated PostgresSQL SQL query")
    reason: str | None