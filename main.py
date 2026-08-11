from fastapi import FastAPI, HTTPException

from app.api.routes.analytics import router as analytics_router
from app.api.exception_handlker import http_exception_handler, general_exception_handler

app = FastAPI(
    title="Self-Correcting Natural Language SQL Analytics API",
    version="1.0.0"
)

app.add_exception_handler(
    HTTPException,
    http_exception_handler
)

app.add_exception_handler(
    Exception,
    general_exception_handler
)

app.include_router(analytics_router, prefix="")

@app.get("/health")
def health_check():
    return {
        "Status": "Healthy"
    }