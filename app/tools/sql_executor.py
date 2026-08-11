from app.database.session import SessionLocal
from sqlalchemy import text

from app.config.logging import get_logger

logger = get_logger(__name__)


def execute_sql(generated_sql: str) -> list[dict]:
    """
    Execute a validated SQL query and return the results
    as a list of dictionaries.
    """

    logger.info("Executing SQL query against PostgreSQL")

    session = SessionLocal()

    try:
        result = session.execute(
            text(generated_sql)
        )

        rows = result.mappings().all()

        query_result = [
            dict(row) for row in rows
        ]

        logger.info(
            "Database query completed successfully. Rows returned: %d",
            len(query_result)
        )

        return query_result

    except Exception:
        logger.exception("Database query execution failed")
        raise

    finally:
        session.close()
        logger.debug("Database session closed")