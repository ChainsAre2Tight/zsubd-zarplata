import random
from datetime import datetime, timedelta
import json
from parser import validate_data, load_data

START_HOUR = 8
BREAK_HOUR = 14
END_HOUR = 18

def create_time(start_hour: int, end_hour: int) -> str:
    hour = random.randint(start_hour, end_hour)
    minute = random.randint(0, 59)
    second = random.randint(0, 59)
    return f'{hour}:{minute}:{second} MSK'

def create_date(base_date: datetime, backwards_shif_in_days: int):
    new_date = base_date - timedelta(days=backwards_shif_in_days)
    new_day = '-'.join(str(new_date).split()[0].split('-')[::-1])
    return new_day
    

def create_workday(base_date: datetime, backwards_shif_in_days: int) -> dict:
    global START_HOUR, BREAK_HOUR, END_HOUR
    day = {
        'workday_date': create_date(base_date=base_date, backwards_shif_in_days=backwards_shif_in_days),
        'entry_time': create_time(START_HOUR, BREAK_HOUR-1),
        'exit_time': create_time(BREAK_HOUR, END_HOUR)
    }
    return day

def create_workmonth():
    now_date = datetime.today()

    res = []
    for shift in range(28):
        res.append(create_workday(now_date, shift))
    
    return res

def append_workmonth_to_json():
    data = load_data()

    for i in range(len(data['employees'])):
        data['employees'][i]['workdays'] = create_workmonth()
    
    validate_data(data=data)
    with open('data.json', 'w') as file:
        json.dump(data, file, indent=4)

if __name__ == '__main__':
    append_workmonth_to_json()