
import psycopg2
from fastapi import Depends
from typing import Annotated

import backend.connection as c


def _connect_to_db() -> psycopg2.extensions.connection:
    conn_data = c.ConnectionDataFactory.create()
    connection_promise = c.ConnectionFactory.create(conn_data)
    with connection_promise() as conn:
        return conn


get_db_connection = Annotated[psycopg2.extensions.connection, Depends(_connect_to_db)]
