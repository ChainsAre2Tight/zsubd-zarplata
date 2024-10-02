class BaseModel:
    insert: str

class Employee(BaseModel):
    insert = 'INSERT INTO employee (fio, payment_method, receipt_address) VALUES (%s, %s, %s)'




class Inserter:

    def __init__(self, cursor):
        self.cursor = cursor

    def insert_row(self, target: object, data: dict):
        self.cursor.execute(target.insert)
    
    def insert_rows(self, target: object, data: list[dict]):
        ...
