from typing import Annotated, Any, TypedDict
from app.schemas.validation import SQLValidationResult
from app.schemas.result_analyzer import ResultAnalysis
from app.schemas.executive_summary import ExecutiveSummary
from app.schemas.response import AnalyticsResponse

class AgentState(TypedDict):
    """
    Shared state passed between all LangGraph nodes
    """

    # user input
    question: str

    # Database Ubderstanding
    schema_context: str | None
    database_schema: dict[str, list[dict]]

    # Business Understanding
    business_context: str | None

    # SQL
    generated_sql: str | None
    validation_result: SQLValidationResult | None

    # Query Execution
    query_result: list[dict[str, Any]] | None

    # Result Analysis
    result_analysis: ResultAnalysis | None

    # Visualization
    chart_config: dict[str, Any] | None

    # Summary / Output
    executive_summary: ExecutiveSummary | None

    # System

    # Error Handling
    error_message: str | None
    retry_count: int

    # Observability
    execution_time: float | None

    # Debugging
    correction_history: list[str]

    final_response: AnalyticsResponse