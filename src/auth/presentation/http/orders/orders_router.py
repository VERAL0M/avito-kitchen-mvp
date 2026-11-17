from fastapi import APIRouter
from auth.presentation.http.orders.cancel_order import cancel_order_router
from auth.presentation.http.orders.create_order import create_order_router
from auth.presentation.http.orders.confirm_order import confirm_order_router
from auth.presentation.http.orders.find_order import find_order_router
from auth.presentation.http.orders.list_orders import list_orders_router

orders_router = APIRouter(
    prefix="/orders",
    tags = ["Orders"],
)

orders_sub_routers = (
    cancel_order_router,
    create_order_router,
    confirm_order_router,
    find_order_router,
    list_orders_router,
)

for router in orders_sub_routers:
    orders_router.include_router(router)
