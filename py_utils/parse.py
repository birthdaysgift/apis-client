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
    object_type: ObjectType | None = None


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
    parse_schema_json(data).model_dump_json()



def get_schema_json(source):
    introspection_query_body = {
        "operationName":"IntrospectionQuery",
        "query": get_introspection_query(),
    }
    response = requests.post(source, json=introspection_query_body)
    print(response.status_code)
    (Path(__file__).parent / "api.json").write_text(json.dumps(response.json(), indent=4))
    return response.json()


def parse_schema_json(data):
    types = {t["name"]: t for t in data["data"]["__schema"]["types"]}

    for main_type in ("Query", "Mutation", "Introspection"):
        type_data = types[main_type]
        if type_data is None:
            continue

        # TODO: now it parses only "Query" but should parse all main types
        return parse_type(type_data, types, required=False)



def parse_type(type_data, types, *, required):

    if type_data["kind"] == "SCALAR":
        return Type(scalar_type=ScalarType(name=type_data["name"], required=required))

    if type_data["kind"] == "NON_NULL":
        return parse_type(type_data["ofType"], types, required=True)

    if type_data["kind"] == "OBJECT":
        fields = []
        for field in types[type_data["name"]]["fields"]:
            field_type = parse_type(field["type"], types, required=False)
            fields.append(Field(name=field["name"], type_=field_type))
        return Type(object_type=ObjectType(name=type_data["name"], fields=fields, required=required))

    if type_data["kind"] == "LIST":
        list_type = parse_type(type_data["ofType"], types, required=False)
        return Type(ListType(type_=list_type, required=required))


if __name__ == "__main__":
    main()

