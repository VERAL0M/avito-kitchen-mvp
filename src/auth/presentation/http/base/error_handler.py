from functools import partial
from typing import cast

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette import status as code

from auth.application.errors import (
    OrderCancelError,
    OrderConfirmError,
    OrderFindError,
    OrderRequestError,
)
from auth.domain.errors import (
    EmptyOrderError,
    Error,
    InvalidOrderItemError,
)


class HTTPError(Error): ...


async def validate(_: Request, error: Exception, status: int) -> JSONResponse:
    error = cast(HTTPError, error)
    return JSONResponse(content={"message": error.message}, status_code=status)


def init_error_handlers(app: FastAPI) -> None:
    app.add_exception_handler(
        OrderRequestError, partial(validate, status=code.HTTP_400_BAD_REQUEST)
    )
    app.add_exception_handler(
        OrderCancelError, partial(validate, status=code.HTTP_409_CONFLICT)
    )
    app.add_exception_handler(
        OrderFindError, partial(validate, status=code.HTTP_404_NOT_FOUND)    
    )
    app.add_exception_handler(
        OrderConfirmError, partial(validate, status=code.HTTP_409_CONFLICT)
    )
    app.add_exception_handler(
        EmptyOrderError, partial(validate, status=code.HTTP_400_BAD_REQUEST)
    )
    app.add_exception_handler(
        InvalidOrderItemError, partial(validate, status=code.HTTP_400_BAD_REQUEST)
    )
