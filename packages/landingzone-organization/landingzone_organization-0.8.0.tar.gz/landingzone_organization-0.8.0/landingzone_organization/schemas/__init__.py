import os
import yaml
from jsonschema import validate

from landingzone_organization.account import Account


class InvalidSchemaException(Exception):
    def __init__(self, file: str, message: str):
        self.file = file
        self.message = message
        super().__init__(self.message)


def load_schema(file: str) -> dict:
    with open(file, "r") as f:
        return yaml.safe_load(f)


def safe_load_file(schema: dict, file_path: str) -> dict:
    try:
        with open(file_path, "r") as f:
            data = yaml.safe_load(f)
            validate(instance=data, schema=schema)
    except Exception as exc:
        raise InvalidSchemaException(file_path, str(exc))

    return data


def environment_resolver(path: str) -> Account:
    data = safe_load_file(EnvironmentSchema, path)

    return Account(
        name=data["Name"],
        account_id=data["AccountId"],
    )


schema_path = os.path.dirname(os.path.abspath(__file__))
WorkloadSchema = load_schema(os.path.join(schema_path, "workload.yaml"))
EnvironmentSchema = load_schema(os.path.join(schema_path, "environment.yaml"))
