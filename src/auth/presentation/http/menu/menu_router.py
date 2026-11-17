from fastapi import APIRouter

menu_router = APIRouter(prefix="/restaurants", tags=["Restaurants"])


@menu_router.get("/")
async def list_restaurants() -> list[dict[str, str]]:
    """Return the single restaurant connected during the MVP."""
    return [{"id": "demo-cafe", "name": "Demo Cafe"}]


@menu_router.get("/{restaurant_id}/menu")
async def get_menu(restaurant_id: str) -> dict[str, object]:
    """Return a fixed menu; the restaurant catalog is out of scope for the MVP."""
    return {
        "restaurant_id": restaurant_id,
        "items": [
            {"name": "Маргарита", "price": "450.00"},
            {"name": "Американо", "price": "180.00"},
        ],
    }
