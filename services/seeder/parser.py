
import json
from jsonschema import validate

with open('schema.json') as schema_file:
    schema = json.load(schema_file)
    with open('data.json') as data_file:
        data = json.load(data_file)
        validate(instance=data, schema=schema)

