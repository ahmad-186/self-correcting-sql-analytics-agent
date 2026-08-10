from app.database.session import SessionLocal
from sqlalchemy import text

def execute_sql(generated_sql: str) -> list[dict]:
    """
    Execute a validated SQL query and return the results
    as a list of dictionaries.
    """

    session = SessionLocal()

    try:
        result = session.execute(
            text(generated_sql)
        )

        rows = result.mappings().all()

        return [
            dict(row) for row in rows
        ]

    finally:
        session.close()