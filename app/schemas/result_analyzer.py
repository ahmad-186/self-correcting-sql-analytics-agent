from pydantic import BaseModel

class ResultAnalysis(BaseModel):

    row_count: int
    column_names: list[str]
    numeric_columns: list[str]
    categorical_columns: list[str]
    datetime_columns: list[str]
    is_empty: bool