from __future__ import annotations

from enum import Enum

from pydantic import BaseModel

import json
from pathlib import Path

import requests
from graphql import get_introspection_query

# from py_utils.sdl_schema import ScalarType, ObjectType, ListType, Field

class Type(BaseModel):
    scalar_type: ScalarType | None = None
    list_type: ListType | None = None
    object_name: str | None = None


class Field(BaseModel):
    name: str
    type_: Type


class ObjectType(BaseModel):
    name: str
    fields: list[Field]
    required: bool


class ScalarType(BaseModel):
    name: ScalarName
    required: bool


class ListType(BaseModel):
    type_: Type
    required: bool


class ScalarName(Enum):
    BOOLEAN = "Boolean"
    FLOAT = "Float"
    ID = "ID"
    INT = "Int"
    STRING = "String"


def main():
    data = get_schema_json("http://localhost:5000/graphql")
    types = get_types(data)
    print(parse_type("Character", types, required=True).model_dump_json())


def get_schema_json(source):
    introspection_query_body = {
        "operationName":"IntrospectionQuery",
        "query": get_introspection_query(),
    }
    response = requests.post(source, json=introspection_query_body)
    print(response.status_code)
    (Path(__file__).parent / "api.json").write_text(json.dumps(response.json(), indent=4))
    return response.json()


def get_types(data):
    return {t["name"]: t for t in data["data"]["__schema"]["types"]}


def parse_type(type_name, types, *, required):
    type_data = types[type_name]
    fields = []
    for field in types[type_data["name"]]["fields"]:
        field_type = parse_field(field["type"], types, required=False)
        try:
            fields.append(Field(name=field["name"], type_=field_type))
        except Exception as e:
            print("exc")
    return ObjectType(name=type_data["name"], fields=fields, required=required)


def parse_field(field_data, types, required):
    if field_data["kind"] == "SCALAR":
        return Type(scalar_type=ScalarType(name=field_data["name"], required=required))

    if field_data["kind"] == "NON_NULL":
        return parse_field(field_data["ofType"], types, required=True)

    if field_data["kind"] == "LIST":
        list_type = parse_field(field_data["ofType"], types, required=False)
        return Type(list_type=ListType(type_=list_type, required=required))

    if field_data["kind"] == "OBJECT":
        return Type(object_name=field_data["name"])

    raise AssertionError(f"Unknown field type. field_data: {field_data}")


if __name__ == "__main__":
    main()

