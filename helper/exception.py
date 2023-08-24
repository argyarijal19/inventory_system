from fastapi import (
    FastAPI,
    status
)
from fastapi.exceptions import (
    RequestValidationError
)
from fastapi.responses import JSONResponse


def ExceptionHandler(app: FastAPI) -> None:
    @app.exception_handler(RequestValidationError)
    async def http_validation_exception_handler(request, exc: RequestValidationError):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                'code': status.HTTP_400_BAD_REQUEST,
                'success': False,
                'message': f'{exc.errors()[0]["msg"]} at {exc.errors()[0]["loc"][0]} need {exc.errors()[0]["loc"][1]} param',
                'data': None
            }
        )

    @app.exception_handler(RequestValidationError)
    async def http_validation_exception_handler(request, exc: RequestValidationError):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                'code': status.HTTP_400_BAD_REQUEST,
                'success': False,
                'message': f'{exc.errors()[0]["msg"]} at {exc.errors()[0]["loc"][0]} need {exc.errors()[0]["loc"][1]} param',
                'data': None
            }
        )

    @app.exception_handler(Exception)
    async def http_internal_server_error_exception_handler(request, exc: Exception):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'success': False,
                'message': str(exc),
                'data': None
            }
        )
