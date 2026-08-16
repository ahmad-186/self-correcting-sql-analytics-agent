from pydantic import BaseModel


class NumericSummary(BaseModel):
    min: float | None = None
    max: float | None = None
    average: float | None = None
    total: float | None = None


class ResultAnalysis(BaseModel):
    row_count: int
    column_names: list[str]
    numeric_columns: list[str]
    categorical_columns: list[str]
    datetime_columns: list[str]
    is_empty: bool
    numeric_summary: dict[str, NumericSummary] = {}

    highest_value: dict | None = None
    lowest_value: dict | None = None