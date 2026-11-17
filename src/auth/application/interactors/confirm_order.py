from dataclasses import dataclass
from auth.application.interfaces.order_repository import OrderRepository
from auth.application.interfaces.transaction_manager import TransactionManager
from auth.domain.entities.order import Order, OrderId
from auth.application.errors import OrderConfirmError, OrderFindError
from auth.domain.errors import OrderStateError



@dataclass
class ConfirmOrderRequest:
    order_id: OrderId


@dataclass
class ConfirmOrderResponse:
    order: Order


class ConfirmOrderInteractor:
    def __init__(
        self,
        order_repository: OrderRepository,
        transaction_manager: TransactionManager,
    ):
        self._order_repository = order_repository
        self._transaction_manager = transaction_manager
    
    async def __call__(self, request_data: ConfirmOrderRequest) -> ConfirmOrderResponse:
        order: Order | None = await self._order_repository.get_by_id(order_id=request_data.order_id)
        if order is None:
            raise OrderFindError("Order not found")
    
        try:
            order.confirm()
        except OrderStateError as error:
            raise OrderConfirmError(str(error)) from error
    
        await self._transaction_manager.commit()
    
    
        return ConfirmOrderResponse(order=order)
        
    
