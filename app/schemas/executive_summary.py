from pydantic import BaseModel

class ExecutiveSummary(BaseModel):

    summary: str
    key_insights: list[str]