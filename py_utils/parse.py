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


class Field(BaseModel):
    name: str
    scalar_type: ScalarType | None = None
    list_type: ListType | None = None
    object_type: ObjectType | None = None
    args: list[Arg]


class Arg(BaseModel):
    name: str
    scalar_type: ScalarType | None = None
    list_type: ListType | None = None
    object_type: ObjectType | None = None


class ObjectType(BaseModel):
    name: str
    required: bool


class ScalarType(BaseModel):
    name: ScalarName
    required: bool


class ListType(BaseModel):
    scalar_type: ScalarType | None = None
    list_type: ListType | None = None
    object_type: ObjectType | None = None
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
    print(parse_object("Query", objects, required=True).model_dump_json(exclude_unset=True))


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
        args = []
        for arg in field["args"]:
            arg_type = parse_field(arg["type"], types, required=False)
            if isinstance(arg_type, ScalarType):
                args.append(Arg(name=arg["name"], scalar_type=arg_type))
                continue
            if isinstance(arg_type, ListType):
                args.append(Arg(name=arg["name"], list_type=arg_type))
                continue
            if isinstance(arg_type, ObjectType):
                args.append(Arg(name=arg["name"], object_type=arg_type))
                continue
            raise AssertionError(f"Unknown arg type: {type(arg_type)}, {arg_type}")

        field_type = parse_field(field["type"], types, required=False)

        if isinstance(field_type, ScalarType):
            fields.append(Field(name=field["name"], scalar_type=field_type, args=args))
            continue
        if isinstance(field_type, ListType):
            fields.append(Field(name=field["name"], list_type=field_type, args=args))
            continue
        if isinstance(field_type, ObjectType):
            fields.append(Field(name=field["name"], object_type=field_type, args=args))
            continue

        raise AssertionError(f"Unknown field type: {type(field_type)}, {field_type}")


    return Object(name=type_data["name"], fields=fields)


def parse_field(field_data, types, required):
    if field_data["kind"] == "SCALAR":
        return ScalarType(name=field_data["name"], required=required)

    if field_data["kind"] == "NON_NULL":
        return parse_field(field_data["ofType"], types, required=True)

    if field_data["kind"] == "LIST":
        list_type = parse_field(field_data["ofType"], types, required=False)
        if isinstance(list_type, ScalarType):
            return ListType(scalar_type=list_type, required=required)
        if isinstance(list_type, ListType):
            return ListType(list_type=list_type, required=required)
        if isinstance(list_type, ObjectType):
            return ListType(object_type=list_type, required=required)
        raise AssertionError(f"Unknown field type: {type(list_type)}, {list_type}")

    if field_data["kind"] in ["OBJECT", "INPUT_OBJECT"]:
        return ObjectType(name=field_data["name"], required=required)

    raise AssertionError(f"Unknown field type. field_data: {field_data}")


if __name__ == "__main__":
    main()

