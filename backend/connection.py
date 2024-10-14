

import psycopg2
import os
import dataclasses
from collections.abc import Callable


@dataclasses.dataclass(frozen=True)
class ConnectionData:
    host: str
    user: str
    password: str
    database: str
    port: int


class ConnectionDataFactory:

    @staticmethod
    def create() -> ConnectionData:
        host = os.getenv('DB_HOST')
        assert host is not None, 'Missing DB_HOST env variable'
        user = os.getenv('DB_USER')
        assert user is not None, 'Missing DB_USER env variable'
        password = os.getenv('DB_PASSWORD')
        assert password is not None, 'Missing DB_PASSWORD env variable'
        database = os.getenv('DB_NAME')
        assert database is not None, 'Missing DB_NAME env variable'
        port = os.getenv('DB_PORT')
        assert port is not None, 'Missing DB_PORT env variable'
        return ConnectionData(
            host=host,
            user=user,
            password=password,
            database=database,
            port=port,
        )


class ConnectionDataFactoryMock(ConnectionDataFactory):

    @staticmethod
    def create() -> ConnectionData:
        return ConnectionData(
            host='localhost',
            user='admin',
            password='supersecretpwd',
            database='zarplata',
            port=5435
        )


class ConnectionFactory:

    @staticmethod
    def create(connection_data: ConnectionData) -> Callable[..., psycopg2.extensions.connection]:
        return lambda: psycopg2.connect(
        host=connection_data.host,
        user=connection_data.user,
        password=connection_data.password,
        database=connection_data.database,
        port=connection_data.port
    )
