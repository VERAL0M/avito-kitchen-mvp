from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, status, Query

from auth.application.interactors.list_order import StatusFilterOrderRequest, StatusFilterOrderInteractor, StatusFilterOrderResponse
from auth.domain.orders_status import OrderStatus

list_orders_router = APIRouter()

@list_orders_router.get(
    "/",
    status_code=status.HTTP_200_OK,
)


@inject
async def list_orders(
    interactor: FromDishka[StatusFilterOrderInteractor],
    status: OrderStatus | None = Query(default=None),
    limit: int | None = Query(default=None, ge=1, le=100),
    offset: int | None = Query(default=None, ge=0),
    
) -> StatusFilterOrderResponse:
    request_data = StatusFilterOrderRequest(status=status, limit=limit, offset=offset)
    return await interactor(request_data)
    