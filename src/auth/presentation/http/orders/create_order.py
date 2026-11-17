from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, status

from auth.application.interactors.create_order import CreateOrderInteractor, CreateOrderRequest, CreateOrderResponse


create_order_router = APIRouter()


@create_order_router.post(
    "/",
    status_code=status.HTTP_201_CREATED
)

@inject
async def create_order(
    request_data: CreateOrderRequest,
    interactor: FromDishka[CreateOrderInteractor]
) -> CreateOrderResponse:
    return await interactor(request_data)