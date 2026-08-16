from datetime import date, datetime
from decimal import Decimal
from typing import Any


def normalize_value(value: Any) -> Any:
    """Convert database-specific values into JSON-friendly Python values."""

    if isinstance(value, Decimal):
        return float(value)

    if isinstance(value, (datetime, date)):
        return value.isoformat()

    return value


def normalize_query_result(
    query_result: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    """Normalize all values returned by the database."""

    return [
        {
            column: normalize_value(value)
            for column, value in row.items()
        }
        for row in query_result
    ]