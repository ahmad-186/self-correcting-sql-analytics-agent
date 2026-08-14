from fastapi import APIRouter, HTTPException

from app.graph.graph import graph
from app.api.schema.analytics import AnalyticsRequest
from app.api.schema.errors import ErrorResponse
from app.config.logging import get_logger

logger = get_logger(__name__)

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"]
)

@router.post(
    "/query",
    summary="Execute a natural-language analytics query",
    description="""
    Accepts a business question in natural language, generates and
    validates SQL, executes the query, analyzes the result, recommends
    a visualization, and returns an executive summary.
    """,
    responses={
        400: {"model": ErrorResponse},
        422: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
)
def analytics_query(request: AnalyticsRequest):

    logger.info("Analytics Request received: %s", request.question)

    initial_state = {
        "question": request.question,
        "retry_count": 0
    }
        
    result = graph.invoke(initial_state)

    logger.info("Analytics graph execution completed.")

    final_response = result.get("final_response")

    if final_response is None:
        logger.error("Analytics graph produced no final response.")
        raise HTTPException(
            status_code=500,
            detail="Analytics graph didn't produce a final response"
        )

    logger.info("Analytics request completed successfully.")

    return final_response