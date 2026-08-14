from decimal import Decimal
from datetime import datetime

from app.tools.result_analyzer import analyze_result

def test_analyze_empty_result():
    result = analyze_result([])

    assert result.row_count == 0
    assert result.column_names == []
    assert result.numeric_columns == []
    assert result.categorical_columns == []
    assert result.datetime_columns == []
    assert result.is_empty is True

def test_analyze_numeric_and_categorical_columns():
    query_result = [
        {
            "city": "Peshawar",
            "total_sales": Decimal("250.00"),
        },
        {
            "city": "Lahore",
            "total_sales": Decimal("300.00"),
        },
    ]

    result = analyze_result(query_result)

    assert result.row_count == 2
    assert result.column_names == ["city", "total_sales"]

    assert "total_sales" in result.numeric_columns
    assert "city" in result.categorical_columns

    assert result.datetime_columns == []
    assert result.is_empty is False

def test_analyze_datetime_column():
    query_result = [
        {
            "order_date": datetime(2026, 8, 1, 10, 30),
            "total_sales": Decimal("500.00"),
        }
    ]

    result = analyze_result(query_result)

    assert "order_date" in result.datetime_columns
    assert "total_sales" in result.numeric_columns

def test_id_columns_are_categorical():
    query_result = [
        {
            "customer_id": 1,
            "full_name": "Ahmad Shahzad",
        },
        {
            "customer_id": 2,
            "full_name": "Ali Khan",
        },
    ]

    result = analyze_result(query_result)

    assert "customer_id" in result.categorical_columns
    assert "full_name" in result.categorical_columns