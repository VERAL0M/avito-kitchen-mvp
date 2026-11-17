from decimal import Decimal
from uuid import UUID

import pytest

from auth.domain.orders_status import OrderStatus
from auth.domain.entities.order import create_order
from auth.domain.entities.order_item import (
    OrderId,
    OrderItem,
    PositionId,
    ProductName,
    Quantity,
    UnitPrice,
)
from auth.domain.errors import EmptyOrderError, OrderStateError, InvalidOrderItemError


def test_order_total_amount() -> None:
    order_id = OrderId(UUID("00000000-0000-0000-0000-000000000010"))
    items = [
        
        OrderItem(
            id=PositionId(UUID("00000000-0000-0000-0000-000000000011")),
            order_id=order_id,
            product_name=ProductName("Laptop"),
            quantity=Quantity(2),
            unit_price=UnitPrice(Decimal("2.50"))

        ),
        OrderItem(
            id=PositionId(UUID("00000000-0000-0000-0000-000000000012")),
            order_id=order_id,
            product_name=ProductName("keyboard"),
            quantity=Quantity(3),
            unit_price=UnitPrice(Decimal("4.53"))
       
        ),
    ]
    order = create_order(id=order_id, items=items)

    assert order.total_amount == Decimal("18.59")


def test_create_order_empty_items() -> None:
    order_id = OrderId(UUID("00000000-0000-0000-0000-000000000020"))

    with pytest.raises(EmptyOrderError, match="Order must have at least one item."):
        create_order(id=order_id, items=[])


def test_confirm_error_status_not_new() -> None:
    order_id = OrderId(UUID("00000000-0000-0000-0000-000000000030"))

    items = [
        OrderItem(
            id=PositionId(UUID("00000000-0000-0000-0000-000000000011")),
            order_id=order_id,
            product_name=ProductName("Laptop"),
            quantity=Quantity(2),
            unit_price=UnitPrice(Decimal("2.50"))
        )
    ]
    order = create_order(id=order_id, items=items)
    order.status = OrderStatus.CANCELED

    with pytest.raises(OrderStateError, match="Only new orders can be confirmed."):
        order.confirm()


def test_confirm() -> None:
    order_id = OrderId(UUID("00000000-0000-0000-0000-000000000040"))

    items = [
        OrderItem(
            id=PositionId(UUID("00000000-0000-0000-0000-000000000011")),
            order_id=order_id,
            product_name=ProductName("Laptop"),
            quantity=Quantity(2),
            unit_price=UnitPrice(Decimal("2.50"))
        )
    ]
    order = create_order(id=order_id, items=items)
    
    order.confirm()
    assert order.status == OrderStatus.CONFIRMED


def test_cancel_error_status_not_new() -> None:
    order_id = OrderId(UUID("00000000-0000-0000-0000-000000000050"))

    items = [
        OrderItem(
            id=PositionId(UUID("00000000-0000-0000-0000-000000000011")),
            order_id=order_id,
            product_name=ProductName("Laptop"),
            quantity=Quantity(2),
            unit_price=UnitPrice(Decimal("2.50"))
        )
    ]
    order = create_order(id=order_id, items=items)
    order.status = OrderStatus.CONFIRMED

    with pytest.raises(OrderStateError, match="Only new orders can be cancelled."):
        order.cancel(reason="test")


def test_cancel() -> None:
    order_id = OrderId(UUID("00000000-0000-0000-0000-000000000060"))

    items = [
        OrderItem(
            id=PositionId(UUID("00000000-0000-0000-0000-000000000011")),
            order_id=order_id,
            product_name=ProductName("Laptop"),
            quantity=Quantity(2),
            unit_price=UnitPrice(Decimal("2.50"))
        )
    ]
    order = create_order(id=order_id, items=items)
    
    order.cancel(reason="test")
    assert order.status == OrderStatus.CANCELED
    assert order.cancel_reason == "test"


def test_cancel_error_empty_reason() -> None:
    order_id = OrderId(UUID("00000000-0000-0000-0000-000000000070"))

    items = [
        OrderItem(
            id=PositionId(UUID("00000000-0000-0000-0000-000000000011")),
            order_id=order_id,
            product_name=ProductName("Laptop"),
            quantity=Quantity(2),
            unit_price=UnitPrice(Decimal("2.50"))
        )
    ]
    order = create_order(id=order_id, items=items)


    with pytest.raises(OrderStateError, match="The cancellation reason cannot be an empty string."):
        order.cancel(reason="")



def test_order_item_quantity() -> None:
    order_id = OrderId(UUID("00000000-0000-0000-0000-000000000080"))
    with pytest.raises(InvalidOrderItemError, match="Quantity must be greater than zero."):
        OrderItem(
            id=PositionId(UUID("00000000-0000-0000-0000-000000000011")),
            order_id=order_id,
            product_name=ProductName("Laptop"),
            quantity=Quantity(0),
            unit_price=UnitPrice(Decimal("2.50"))
        )


def test_order_item_unit_price() -> None:
    order_id = OrderId(UUID("00000000-0000-0000-0000-000000000090"))
    with pytest.raises(
        InvalidOrderItemError, match="The price must be greater than zero."
    ):
        OrderItem(
            id=PositionId(UUID("00000000-0000-0000-0000-000000000011")),
            order_id=order_id,
            product_name=ProductName("Laptop"),
            quantity=Quantity(10),
            unit_price=UnitPrice(Decimal("0"))
        )
