from typing import AsyncIterable

from dishka import Provider, Scope, from_context, provide
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from starlette.requests import Request

from auth.application.interfaces.transaction_manager import TransactionManager
from auth.entrypoint.config import Config
from auth.infrastructure.adapters.transaction_manager_sqla import TransactionManagerImpl

from auth.infrastructure.adapters.order_repository_sql import OrderRepositorySql
from auth.application.interfaces.order_repository import OrderRepository
from auth.infrastructure.adapters.order_id_generator_uuid import OrderIdGeneratorImpl
from auth.application.interfaces.order_id_generator import OrderIdGenerator
from auth.infrastructure.adapters.position_id_generator_uuid import PositionIdGeneratorImpl
from auth.application.interfaces.position_id_generator import PositionIdGenerator


class SqlaProvider(Provider):
    @provide(scope=Scope.APP)
    def provide_engine(self, config: Config) -> AsyncEngine:
        return create_async_engine(config.postgres_config.uri)

    @provide(scope=Scope.APP)
    def provide_sessionmaker(
        self, engine: AsyncEngine
    ) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(bind=engine, expire_on_commit=False)

    @provide(scope=Scope.REQUEST, provides=AsyncSession)
    async def provide_session(
        self, sessionmaker: async_sessionmaker[AsyncSession]
    ) -> AsyncIterable[AsyncSession]:
        async with sessionmaker() as session:
            yield session

    order_repository_sql = provide(
        OrderRepositorySql, scope=Scope.REQUEST, provides=OrderRepository
        )
    transaction_manager = provide(
        TransactionManagerImpl, scope=Scope.REQUEST, provides=TransactionManager
    )


class IdGeneratorsProvider(Provider):
    order_id_generator =  provide(
        OrderIdGeneratorImpl, scope=Scope.REQUEST, provides=OrderIdGenerator)

    position_id_generator = provide(
      PositionIdGeneratorImpl, scope=Scope.REQUEST, provides=PositionIdGenerator
    )
    
    


class ConfigProvider(Provider):
    config = from_context(provides=Config, scope=Scope.APP)
