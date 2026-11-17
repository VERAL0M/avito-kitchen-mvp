from dataclasses import dataclass
from uuid import UUID

from auth.application.errors import OrderFindError
from auth.application.interfaces.order_repository import OrderRepository
from auth.domain.entities.order import Order, CreatedAt, UpdatedAt, CancelReason
from auth.domain.entities.order_item import OrderItem, OrderId, ProductName, Quantity, UnitPrice, PositionId
from auth.domain.orders_status import OrderStatus



@dataclass
class FindOrderRequest:
    order_id: OrderId

@dataclass
class FindOrderResponse:
    id: OrderId
    items: list[OrderItem]
    status: OrderStatus
    created_at: CreatedAt
    updated_at: UpdatedAt
    cancel_reason: CancelReason | None


class FindOrderInteractor:
    def __init__(
        self,
        order_repository: OrderRepository,
    ):
        self._order_repository = order_repository

    async def __call__(self, request_data: FindOrderRequest) -> FindOrderResponse:
        order: Order | None = await self._order_repository.get_by_id(order_id=request_data.order_id)
        if order is None:
            raise OrderFindError("Order not found.")

        return FindOrderResponse(
            id=order.id,
            items=order.items,
            status=order.status,
            created_at=order.created_at,
            updated_at=order.updated_at,
            cancel_reason=order.cancel_reason,

        )

        
