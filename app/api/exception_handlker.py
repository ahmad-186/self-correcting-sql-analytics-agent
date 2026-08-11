from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.api.schema.errors import ErrorResponse
from app.config.logging import get_logger

logger = get_logger(__name__)


async def http_exception_handler(
        request: Request,
        exc
):
    logger.warning(
        "HTTP exception | %s %s | status=%s | detail=%s",
        request.method,
        request.url.path,
        exc.status_code,
        exc.detail
    )
    
    error_response = ErrorResponse(
        error="HTTP_ERROR",
        message=str(exc.detail)
    )

    return JSONResponse(
        status_code=exc.status_code,
        content=error_response.model_dump()
    )

async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):
    logger.warning(
        "Request validation failed | %s %s | errors=%s",
        request.method,
        request.url.path,
        exc.errors()
    )

    errors = exc.errors()

    messages = []

    for error in errors:
        field = ".".join(str(location) for location in error["loc"][1:])
        messages.append(
            f"{field}: {error['msg']}"
        )

    return JSONResponse(
        status_code=422,
        content={
            "error": "VALIDATION_ERROR",
            "message": "; ".join(messages)
        }
    )



async def general_exception_handler(
        request: Request,
        exc: Exception
):

    logger.exception(
        "Unhandled application exception | %s %s",
        request.method,
        request.url.path
    )
    
    error_response = ErrorResponse(
        error="INTERNAL_SERVER_ERROR",
        message="An Internal error occured while processing the request."
    )

    return JSONResponse(
        status_code=500,
        content=error_response.model_dump()
    )