from dataclasses import dataclass
from auth.application.interfaces.order_repository import OrderRepository
from auth.application.interfaces.transaction_manager import TransactionManager
from auth.domain.entities.order import Order, CancelReason
from auth.domain.entities.order_item import OrderId
from auth.application.errors import OrderCancelError, OrderFindError
from auth.domain.errors import OrderStateError


@dataclass
class CancelOrderRequest:
    order_id: OrderId
    cancel_reason: CancelReason = CancelReason("Заказ отменён пользователем")


@dataclass
class CancelOrderResponse:
    order: Order


class CancelOrderInteractor:
    def __init__(
        self,
        order_repository: OrderRepository,
        transaction_manager: TransactionManager,
    ):
        self._order_repository = order_repository
        self._transaction_manager = transaction_manager

    async def __call__(self, request_data: CancelOrderRequest) -> CancelOrderResponse:
        order: Order | None = await self._order_repository.get_by_id(order_id=request_data.order_id)
        if order is None:
            raise OrderFindError("Order not found")

        try:
            order.cancel(reason=request_data.cancel_reason)
        except OrderStateError as error:
            raise OrderCancelError(str(error)) from error

        await self._transaction_manager.commit()


        return CancelOrderResponse(order=order)
    
