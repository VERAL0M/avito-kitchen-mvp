from dataclasses import dataclass



from auth.application.interfaces.order_repository import OrderRepository
from auth.application.errors import OrderRequestError
from auth.domain.entities.order import  Order
from auth.domain.orders_status import OrderStatus
    


@dataclass
class StatusFilterOrderRequest:
    status: OrderStatus | None
    limit: int | None = None
    offset: int | None = None

@dataclass
class StatusFilterOrderResponse:
    items: list[Order] 

class StatusFilterOrderInteractor:
    def __init__(
        self,
        order_repository: OrderRepository,
        ):
        self._order_repository = order_repository

    async def __call__(self, 
                        request_data: StatusFilterOrderRequest, 
                        ) -> StatusFilterOrderResponse:
        if request_data.offset is not None and request_data.offset < 0:
            raise OrderRequestError("Invalid offset value")

        if request_data.limit is not None and (request_data.limit < 1 or request_data.limit > 100):
            raise OrderRequestError("Invalid limit value")
        
        

        list_order = await self._order_repository.list_all(
            status=request_data.status,
            limit=request_data.limit,
            offset=request_data.offset,
        )
        
        return StatusFilterOrderResponse(items=list_order)

