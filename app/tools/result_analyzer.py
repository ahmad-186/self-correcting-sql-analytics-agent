from app.schemas.result_analyzer import ResultAnalysis
from typing import Any
from datetime import date, datetime
from decimal import Decimal

def analyze_result(query_result: list[dict[str, Any]]) -> ResultAnalysis:
    """
    Analyze SQL query results and generate metadata for downstream nodes.
    """

    if not query_result:

        return ResultAnalysis(
            row_count=0,
            column_names=[],
            numeric_columns=[],
            categorical_columns=[],
            datetime_columns=[],
            is_empty=True
        )

    row_count = len(query_result)
    column_names = list(query_result[0].keys())

    # column_names = []
    # for col in query_result[0].keys():
    #     column_names.append(col)

    numeric_columns = []
    categorical_columns = []
    datetime_columns = []

    # Detect the column type
    for column in column_names:

        if column.endswith("_id"):
            categorical_columns.append(column)
            continue

        sample_value = None

        # Find the first non-null value
        for row in query_result:
            if row[column] is not None:
                sample_value = row[column]
                break

        if sample_value is None:
            continue

        if isinstance(sample_value, (int, float, Decimal)):
            numeric_columns.append(column)
        elif isinstance(sample_value, (date, datetime)):
            datetime_columns.append(column)
        else:
            categorical_columns.append(column)

    return ResultAnalysis(
        row_count=row_count,
        column_names=column_names,
        numeric_columns=numeric_columns,
        categorical_columns=categorical_columns,
        datetime_columns=datetime_columns,
        is_empty=False
    )