from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.analytics import router as analytics_router
from app.api.exception_handlker import http_exception_handler, general_exception_handler, validation_exception_handler
from app.config.logging import get_logger, setup_logging

setup_logging()

logger = get_logger(__name__)

app = FastAPI(
    title="Self-Correcting Natural Language SQL Analytics API",
    description="""
    Natural-language analytics API that converts business questions
    into validated SQL queries, executes them against PostgreSQL,
    analyzes results, recommends visualizations, and generates
    executive summaries.
    """,
    version="1.0.0",
    contact={
        "name": "Analytics API"
    },
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(
    HTTPException,
    http_exception_handler
)

app.add_exception_handler(
    RequestValidationError,
    validation_exception_handler
)

app.add_exception_handler(
    Exception,
    general_exception_handler
)

app.include_router(analytics_router, prefix="")

@app.get(
    "/health",
    summary="Check API health",
    description="Returns the current health status of the analytics API.",
    tags=["Health"]
)
def health_check():

    logger.info("Health check requested")

    return {
        "Status": "Healthy"
    }