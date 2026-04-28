from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.core.exceptions import AppError


def add_exception_handlers(app: FastAPI):
    @app.exception_handler(AppError)
    async def app_error_handler(request: Request, exc: AppError):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "status": "error",
                "message": exc.message,
                "code": exc.__class__.__name__,
            },
        )
