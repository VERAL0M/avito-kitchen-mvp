from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, status

from auth.application.interactors.find_order import FindOrderInteractor, FindOrderRequest, FindOrderResponse
from auth.domain.entities.order_item import  OrderId


find_order_router = APIRouter()

@find_order_router.get(
    "/{order_id}",
    status_code=status.HTTP_200_OK,
)

@inject
async def find_order(
    interactor: FromDishka[FindOrderInteractor],
    order_id: OrderId,
) -> FindOrderResponse:
    request_data = FindOrderRequest(order_id=order_id)
    return await interactor(request_data)

