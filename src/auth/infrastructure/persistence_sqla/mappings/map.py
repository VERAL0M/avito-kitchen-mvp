from auth.infrastructure.persistence_sqla.mappings.order import map_order_table
from auth.infrastructure.persistence_sqla.mappings.order_item import map_create_order_item_table

def map_tables() -> None:
    map_order_table()
    map_create_order_item_table()
    
