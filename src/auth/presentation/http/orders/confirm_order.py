from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, status 

from auth.application.interactors.confirm_order import ConfirmOrderInteractor, ConfirmOrderRequest, ConfirmOrderResponse
from auth.domain.entities.order_item import  OrderId

confirm_order_router = APIRouter()


@confirm_order_router.post(
    "/{order_id}/confirm",
    status_code=status.HTTP_200_OK,
)

@inject
async def confirm_order(
    order_id: OrderId,
    interactor: FromDishka[ConfirmOrderInteractor],
) -> ConfirmOrderResponse:
    request_data = ConfirmOrderRequest(order_id=order_id)
    return await interactor(request_data)

