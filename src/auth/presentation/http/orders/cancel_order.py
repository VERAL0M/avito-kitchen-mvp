from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, status

from auth.application.interactors.cancel_order import CancelOrderInteractor, CancelOrderRequest, CancelOrderResponse
from auth.domain.entities.order_item import  OrderId
from auth.domain.entities.order import CancelReason

cancel_order_router = APIRouter()

@cancel_order_router.post(
    "/{order_id}/cancel",
    status_code = status.HTTP_200_OK,
)

@inject
async def cancel_order(
    order_id: OrderId,
    interactor: FromDishka[CancelOrderInteractor],
) -> CancelOrderResponse:
    request_data = CancelOrderRequest(
        order_id=order_id,
        cancel_reason=CancelReason("Заказ отменён пользователем"),
    )
    return await interactor(request_data)
