from abc import abstractmethod
from typing import Protocol

from auth.domain.entities.order import Order
from auth.domain.entities.order_item import OrderId
from auth.domain.orders_status import OrderStatus


class OrderRepository(Protocol):
    @abstractmethod
    async def add(self, order: Order) -> None: ...

    @abstractmethod
    async def get_by_id(self, order_id: OrderId) -> Order | None: ...

    @abstractmethod
    async def list_all( self,
            status: OrderStatus | None,
            limit: int | None, 
            offset: int | None,
            
            ) -> list[Order]: ...

    
