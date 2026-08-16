from app.schemas.result_analyzer import ResultAnalysis, NumericSummary
from typing import Any
from datetime import date, datetime
from decimal import Decimal
from app.config.logging import get_logger

logger = get_logger(__name__)

def analyze_result(query_result: list[dict[str, Any]]) -> ResultAnalysis:
    """
    Analyze SQL query results and generate metadata for downstream nodes.
    """

    logger.info("Analyzing query result")

    if not query_result:

        logger.info("Query result is empty")

        return ResultAnalysis(
            row_count=0,
            column_names=[],
            numeric_columns=[],
            categorical_columns=[],
            datetime_columns=[],
            is_empty=True,
            numeric_summary={}
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

    logger.debug(
        "Detected columns | numeric=%s | categorical=%s | datetime=%s",
        numeric_columns,
        categorical_columns,
        datetime_columns,
    )

    numeric_summary = {}

    for column in numeric_columns:
        values = [
            row[column]
            for row in query_result
            if row[column] is not None
        ]

        if values:
            numeric_summary[column] = NumericSummary(
                min=float(min(values)),
                max=float(max(values)),
                average=float(sum(values) / len(values)),
                total=float(sum(values))
            )
    highest_value = None
    lowest_value = None

    for column in numeric_columns:
        values = [
            row[column]
            for row in query_result
            if row[column] is not None
        ]

        if not values:
            continue

        max_row = max(
            query_result,
            key=lambda row: (
                row[column]
                if row[column] is not None
                else float("-inf")
            )
        )

        min_row = min(
            query_result,
            key=lambda row: (
                row[column]
                if row[column] is not None
                else float("inf")
            )
        )

        highest_value = {
            "column": column,
            "value": float(max_row[column]),
            "row": max_row,
        }

        lowest_value = {
            "column": column,
            "value": float(min_row[column]),
            "row": min_row,
        }

    return ResultAnalysis(
        row_count=row_count,
        column_names=column_names,
        numeric_columns=numeric_columns,
        categorical_columns=categorical_columns,
        datetime_columns=datetime_columns,
        is_empty=False,
        numeric_summary=numeric_summary,
        highest_value=highest_value,
        lowest_value=lowest_value,
    )
