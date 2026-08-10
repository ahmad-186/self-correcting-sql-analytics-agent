from fastapi import APIRouter, HTTPException

from app.graph.graph import graph
from app.api.schema.analytics import AnalyticsRequest

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"]
)

@router.post("/query")
def analytics_query(request: AnalyticsRequest):

    initial_state = {
        "question": request.question,
        "retry_count": 0
    }

    try:
        result = graph.invoke(initial_state)

        final_response = result.get("final_response")

        if final_response is None:
            raise HTTPException(
                status_code=500,
                detail="Analytics graph didn't produce a final response"
            )

        return final_response

    except HTTPException:
        raise

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Analytics processing failed {str(exc)}"
        )