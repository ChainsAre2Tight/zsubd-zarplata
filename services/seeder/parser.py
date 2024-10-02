
import json
from jsonschema import validate

def load_and_validate() -> dict:
    with open('schema.json') as schema_file:
        schema = json.load(schema_file)
        with open('data.json') as data_file:
            data = json.load(data_file)
            validate(instance=data, schema=schema)
            return data

if __name__ == "__main__":
    load_and_validate()
