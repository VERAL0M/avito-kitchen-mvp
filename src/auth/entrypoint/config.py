from dataclasses import dataclass
from os import getenv


@dataclass
class PostgresConfig:
    host: str
    port: int
    db: str
    user: str
    password: str

    uri: str

    @staticmethod
    def from_env() -> "PostgresConfig":
        host = getenv("POSTGRES_HOST")
        port = getenv("POSTGRES_PORT")
        db = getenv("POSTGRES_DB")
        user = getenv("POSTGRES_USER")
        password = getenv("POSTGRES_PASS")

        uri = f"postgresql+psycopg://{user}:{password}@{host}:{port}/{db}"

        return PostgresConfig(
            uri=uri, host=host, port=port, db=db, user=user, password=password
        )


@dataclass
class Config:
    postgres_config: PostgresConfig


def create_config() -> Config:
    return Config(
        postgres_config=PostgresConfig.from_env(),
    )
