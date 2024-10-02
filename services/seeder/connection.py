import psycopg2
import os

class BaseConnection:
    _host: str
    _user: str
    _password: str
    _database: str
    _port: int

    def __init__(self, host: str, user: str, password: str, database: str, port: int):
        pass

class Connection(BaseConnection):

    def __init__(self, host: str, user: str, password: str, database: str, port: int):
        self._host = host
        self._user = user
        self._password = password
        self._database = database
        self._port = port

    def __enter__(self):
        print('Connecting to database...')
        self.connection = psycopg2.connect(host=self._host, password=self._password, user=self._user, dbname=self._database, port=self._port, options="-c datestyle=ISO,DMY")
        print(f'Connected to database')
        self.cursor = self.connection.cursor()
        return self
    
    def __exit__(self, exception_type, exception_value, exception_traceback):
        self.connection.close()
        print('Connection to database closed')

class ConnectionFactory:

    def __init__(self):
        self.host = os.getenv('DB_HOST')
        assert self.host is not None, 'Missing DB_HOST env variable'
        self.user = os.getenv('DB_USER')
        assert self.user is not None, 'Missing DB_USER env variable'
        self.password = os.getenv('DB_PASSWORD')
        assert self.password is not None, 'Missing DB_PASSWORD env variable'
        self.database = os.getenv('DB_NAME')
        assert self.database is not None, 'Missing DB_NAME env variable'
        self.port = os.getenv('DB_PORT')
        assert self.port is not None, 'Missing DB_PORT env variable'
    
    def create(self, connection_type: BaseConnection) -> BaseConnection:
        return connection_type(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
            port=self.port
        )