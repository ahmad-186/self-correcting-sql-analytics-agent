from app.tools.sql_validator import validate_sql
from app.schemas.validation import ValidationCheck

SCHEMA = {
    "customers": [
        {"column_name": "customer_id", "data_type": "integer"},
        {"column_name": "full_name", "data_type": "character varying"},
        {"column_name": "city", "data_type": "character varying"}
    ],
    "orders": [
        {"column_name": "order_id", "data_type": "integer"},
        {"column_name": "customer_id", "data_type": "integer"},
        {"column_name": "total_amount", "data_type": "numeric"},
    ]
}

def test_valid_select():
    sql = "SELECT customer_id, full_name FROM customers;"

    result = validate_sql(sql, SCHEMA)

    assert result.is_valid is True
    assert result.failed_Check is None

def test_invalid_sql_syntax():
    sql = "SELEC * FROM customers"

    result = validate_sql(sql, SCHEMA)

    assert result.is_valid is False
    assert result.failed_Check == ValidationCheck.SYNTAX


def test_write_query_is_rejected():
    sql = "DELETE FROM customers;"

    result = validate_sql(sql, SCHEMA)

    assert result.is_valid is False
    assert result.failed_Check == ValidationCheck.READ_ONLY


def test_unknown_table_is_rejected():
    sql = "SELECT * FROM products;"

    result = validate_sql(sql, SCHEMA)

    assert result.is_valid is False
    assert result.failed_Check == ValidationCheck.SCHEMA


def test_invalid_postgres_query_is_rejected():
    sql = "SELECT unknown_column FROM customers;"

    result = validate_sql(sql, SCHEMA)

    assert result.is_valid is False
    assert result.failed_Check == ValidationCheck.EXECUTION