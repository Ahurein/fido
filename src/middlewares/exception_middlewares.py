from xml.dom import VALIDATION_ERR

from fastapi.responses import JSONResponse
from fastapi import status, FastAPI, Request
from fastapi.exceptions import RequestValidationError

from src.exceptions.exceptions import NotFoundException


def add_exception_middleware(app: FastAPI):
    @app.exception_handler(NotFoundException)
    async def global_exception_handler(request: Request, ex: NotFoundException):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": str(ex)}
        )

    @app.exception_handler(RequestValidationError)
    async def global_exception_handler(request: Request, ex: NotFoundException):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": ex}
        )

    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, ex: Exception):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "An error occurred!, try again"}
        )
