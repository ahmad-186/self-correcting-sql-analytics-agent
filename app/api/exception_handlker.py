from fastapi import Request
from fastapi.responses import JSONResponse

from app.api.schema.errors import ErrorResponse

async def http_exception_handler(
        request: Request,
        exc
):
    error_response = ErrorResponse(
        error="HTTP_ERROR",
        message=str(exc.detail)
    )

    return JSONResponse(
        status_code=exc.status_code,
        content=error_response.model_dump()
    )


async def general_exception_handler(
        request: Request,
        exc: Exception
):
    error_response = ErrorResponse(
        error="INTERNAL_SERVER_ERROR",
        message="An Internal error occured while processing the request."
    )

    return JSONResponse(
        status_code=500,
        content=error_response.model_dump()
    )