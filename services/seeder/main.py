from dotenv import load_dotenv
from connection import ConnectionFactory, Connection

if __name__ == "__main__":
    load_dotenv()
    factory = ConnectionFactory()
    with factory.create(Connection) as connection:
        print('lox')
