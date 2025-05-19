from __future__ import annotations

from enum import Enum

from pydantic import BaseModel

import json
from pathlib import Path

import requests
from graphql import get_introspection_query


class Object(BaseModel):
    name: str
    fields: list[Field]
    required: bool  # TODO: do we need it ? seems yes, because object can be as a part of a field


class Field(BaseModel):
    name: str
    type_: Type
    args: list[Arg]


class Type(BaseModel):
    scalar_type: ScalarType | None = None
    list_type: ListType | None = None
    object_type: ObjectType | None = None


class Arg(BaseModel):
    name: str
    type_: Type


class ObjectType(BaseModel):
    name: str
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
    objects = get_objects(data)
    print(parse_object("Query", objects, required=True).model_dump_json())


def get_schema_json(source):
    introspection_query_body = {
        "operationName":"IntrospectionQuery",
        "query": get_introspection_query(),
    }
    response = requests.post(source, json=introspection_query_body)
    print(response.status_code)
    (Path(__file__).parent / "api.json").write_text(json.dumps(response.json(), indent=4))
    return response.json()


def get_objects(data):
    return {t["name"]: t for t in data["data"]["__schema"]["types"]}


def parse_object(type_name, types, *, required):
    type_data = types[type_name]
    fields = []
    for field in types[type_data["name"]]["fields"]:
        field_type = parse_field(field["type"], types, required=False)

        args = []
        for arg in field["args"]:
            args.append(
                Arg(
                    name=arg["name"],
                    type_=parse_field(arg["type"], types, required=False)
                )
            )

        try:
            fields.append(Field(name=field["name"], type_=field_type, args=args))
        except Exception as e:
            print('exc')
    return Object(name=type_data["name"], fields=fields, required=required)


def parse_field(field_data, types, required):
    if field_data["kind"] == "SCALAR":
        return Type(scalar_type=ScalarType(name=field_data["name"], required=required))

    if field_data["kind"] == "NON_NULL":
        return parse_field(field_data["ofType"], types, required=True)

    if field_data["kind"] == "LIST":
        list_type = parse_field(field_data["ofType"], types, required=False)
        return Type(list_type=ListType(type_=list_type, required=required))

    if field_data["kind"] in ["OBJECT", "INPUT_OBJECT"]:
        return Type(object_type=ObjectType(name=field_data["name"], required=required))

    raise AssertionError(f"Unknown field type. field_data: {field_data}")


if __name__ == "__main__":
    main()

