from pydantic import BaseModel, field_validator

from datetime import datetime


def validate_date_format(date: str) -> bool:
    try:
        datetime.fromisoformat(date)
    except:
        return False
    return True


class VacationIn(BaseModel):
    begin_date: str
    end_date: str

    @field_validator('begin_date', 'end_date')
    def validate_dates(cls, v: str):
        if not validate_date_format(v):
            raise ValueError('Date is not in ISO8601 format')
        return v