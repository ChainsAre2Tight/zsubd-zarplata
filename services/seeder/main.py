from dotenv import load_dotenv

from connection import ConnectionFactory, Connection
from parser import load_and_validate

if __name__ == "__main__":
    load_dotenv()
    factory = ConnectionFactory()
    data: dict = load_and_validate()
    
    # insert payrates
    for payrate in data['payrates']:
        with factory.create(Connection) as connection:
            cursor = connection.cursor
            cursor.execute(
                'INSERT INTO payrate (job_title, base_rate, commission, salaty_type, payment_period) VALUES (%s, %s, %s, %s, %s)',
                (payrate['job_title'], payrate['base_rate'], payrate['comission'], payrate['salary_type'], payrate['payment_period'])
            )
            print('inserted payrate', payrate['job_title'], payrate['base_rate'], payrate['comission'], payrate['salary_type'], payrate['payment_period'])

    # for each employee
    for employee in data['employees']:
        # insert him
        with factory.create(Connection) as connection:
            cursor = connection.cursor
            cursor.execute(
                'INSERT INTO employee (fio, payment_method, receipt_address) VALUES (%s, %s, %s);',
                (employee['fio'], employee['payment_method'], employee['receipt_address'])
            )
            print('added employee', employee['fio'], employee['payment_method'], employee['receipt_address'])
            
            # query his UUID
            cursor.execute(
                '''SELECT id FROM employee WHERE fio = %s AND receipt_address = %s;''',
                (employee["fio"], employee['receipt_address'])
            )
            employee['id'] = cursor.fetchone()[0]
            print('his uuid is', employee['id'])

            # insert his vacations
            for vacation in employee['vacations']:
                cursor.execute(
                    'INSERT INTO vacation (employee_id, begin_date, end_date) VALUES (%s, %s, %s);',
                    (employee['id'], vacation['start'], vacation['end'])
                )
                print('inserted vacation', employee['id'], vacation['start'], vacation['end'])
            # insert his orders
            for order in employee['orders']:
                cursor.execute(
                    'INSERT INTO fulfilled_order (employee_id, amount, fullfillment_date) VALUES (%s, %s, %s);',
                    (employee['id'], order['amount'], order['date'])
                )
                print('inserted order', employee['id'], order['amount'], order['date'])
            # insert his salary
            cursor.execute(
                'INSERT INTO salary (employee_id, payrate_id) VALUES (%s, %s);',
                (employee['id'], employee['payrateId'])
            )
            print('inserted salary', employee['id'], employee['payrateId'])
            for workday in employee['workdays']:
                cursor.execute(
                    'INSERT INTO workday (employee_id, workday_date, entry_time, exit_time) VALUES (%s, %s, %s, %s);',
                    (employee['id'], workday['workday_date'], workday['entry_time'], workday['exit_time'])
                )

    
