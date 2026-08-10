from pydantic import BaseModel, Field

class AnalyticsRequest(BaseModel):

    question: str = Field(..., min_length=1, description="Natural Language Analytics Question")
    