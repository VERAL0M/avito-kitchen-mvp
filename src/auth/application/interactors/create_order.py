from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID



from auth.application.interfaces.order_id_generator import OrderIdGenerator
from auth.application.interfaces.position_id_generator import PositionIdGenerator
from auth.application.interfaces.order_repository import OrderRepository
from auth.application.interfaces.transaction_manager import TransactionManager
from auth.domain.entities.order_item import (
    OrderItem,
    PositionId,
    ProductName,
    Quantity,
    UnitPrice,
)

from auth.domain.entities.order import (
    OrderId,
    Order,
    OrderStatus,
    create_order,
    )


@dataclass
class OrderItemRequest:
    product_name: str
    quantity: int
    unit_price: Decimal

@dataclass
class CreateOrderRequest:
    items: list[OrderItemRequest]

@dataclass
class CreateOrderResponse:
    order_id: UUID
    status: OrderStatus
    total_amount: Decimal



class CreateOrderInteractor:
    def __init__(self,
        order_repository: OrderRepository,
        order_id_generator: OrderIdGenerator,
        transaction_manager: TransactionManager,
        position_id_generator: PositionIdGenerator,
    ):

        self._order_repository = order_repository
        self._transaction_manager = transaction_manager
        self._order_id_generator = order_id_generator
        self._position_id_generator = position_id_generator

    async def __call__(
        self, request_order_data: CreateOrderRequest
    ) -> CreateOrderResponse:
        order_id: OrderId = self._order_id_generator()
        
        items: list[OrderItem] = []


        for item_request in request_order_data.items:
            position_id: PositionId = self._position_id_generator()
            order_item = OrderItem(
                id=position_id,
                order_id=order_id,
                product_name=ProductName(item_request.product_name),
                quantity=Quantity(item_request.quantity),
                unit_price=UnitPrice(item_request.unit_price),
            )
            items.append(order_item)

        order: Order = create_order(id=order_id, items=items)

        await self._order_repository.add(order=order)
        await self._transaction_manager.commit()

        return CreateOrderResponse(
            order_id=order.id, 
            status=order.status,
            total_amount=order.total_amount,
        )







        
        



    
