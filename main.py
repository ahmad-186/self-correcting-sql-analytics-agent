from fastapi import FastAPI

from app.api.routes.analytics import router as analytics_router

app = FastAPI(
    title="Self-Correcting Natural Language SQL Analytics API",
    version="1.0.0"
)

app.include_router(analytics_router, prefix="")

@app.get("/health")
def health_check():
    return {
        "Status": "Healthy"
    }