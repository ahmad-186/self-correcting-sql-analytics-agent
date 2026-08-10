from pydantic import BaseModel

from app.schemas.result_analyzer import ResultAnalysis
from app.schemas.chart_config import ChartConfig
from app.schemas.executive_summary import ExecutiveSummary

class AnalyticsResponse(BaseModel):
    question: str
    summary: ExecutiveSummary
    chart: ChartConfig
    result: list[dict]