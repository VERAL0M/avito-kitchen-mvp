# Avito.Кухня MVP

Минимальный сервис: пользователь смотрит меню кафе, создаёт заказ, получает его по ID и отменяет. Регистрация и вход не нужны; заказы доступны по случайному UUID.

## Что сделано

- API меню одного демонстрационного заведения: `GET /restaurants/` и `GET /restaurants/demo-cafe/menu`;
- API заказов: создать, получить список и детали, отменить или подтвердить;
- PostgreSQL-миграции для `orders` и `order_items`, OpenAPI в [docs/openapi.yaml](docs/openapi.yaml), схема в [docs/database-schema.md](docs/database-schema.md);
- отдельный сервис `restaurant-demo`, запускаемый вместе со стеком через Docker Compose (`GET http://localhost:8082/health`); `GET /platform-status` показывает его запрос к API площадки.

## Запуск

```bash
docker compose up --build -d
docker compose exec backend alembic upgrade head
```

Основной API: `http://localhost:8001/docs`. Проверка линтера: `ruff check src tests`. Тесты: `PYTHONPATH=src pytest tests/unit/domain/test_order.py`.

## Проверка

В заказ нельзя передать пустой список, нулевое количество или нулевую цену. Новый заказ можно отменить или подтвердить только один раз; неправильное действие возвращает понятную ошибку.
