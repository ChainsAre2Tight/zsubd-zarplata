
import json
from jsonschema import validate

def load_data() -> dict:
    with open('data.json') as data_file:
        data = json.load(data_file)
        return data

def validate_data(data: dict) -> None:
    with open('schema.json') as schema_file:
        schema = json.load(schema_file)
        validate(instance=data, schema=schema)

def load_and_validate() -> dict:
    data = load_data()
    validate_data(data=data)
    return data

if __name__ == "__main__":
    load_and_validate()
