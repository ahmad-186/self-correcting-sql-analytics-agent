from pydantic import BaseModel
from enum import Enum

class ChartType(str, Enum):

    BAR = "bar"
    LINE = "line"
    PIE = "pie"
    SCATTER = "scatter"
    TABLE = "table"
    NONE = "none"

class ChartConfig(BaseModel):
    chart_type: ChartType
    title: str
    x_axis: str | None = None
    y_axis: str | None = None
    data: list[dict]

class ChartRecommendation(BaseModel):

    chart_type: ChartType
    x_axis: str | None = None
    y_axis: str | None = None
    title: str
    reason: str