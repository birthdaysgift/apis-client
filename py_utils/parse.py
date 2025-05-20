from __future__ import annotations

from enum import Enum

from pydantic import BaseModel

import json
from pathlib import Path

import requests
from graphql import get_introspection_query


class Object(BaseModel):
    name: str
    fields: dict[str, Field]


class Field(BaseModel):
    scalar_type: ScalarType | None = None
    list_type: ListType | None = None
    object_type: ObjectType | None = None
    enum_type: EnumType | None = None
    args: dict[str, Arg]


class Arg(BaseModel):
    scalar_type: ScalarType | None = None
    list_type: ListType | None = None
    object_type: ObjectType | None = None
    enum_type: EnumType | None = None


class ObjectType(BaseModel):
    name: str
    required: bool


class ScalarType(BaseModel):
    name: ScalarName
    required: bool


class ListType(BaseModel):
    required: bool
    scalar_type: ScalarType | None = None
    list_type: ListType | None = None
    object_type: ObjectType | None = None
    enum_type: EnumType | None = None


class EnumType(BaseModel):
    name: str
    required: bool
    values: list[str]


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
    (Path(__file__).parent / "api.json").write_text(json.dumps(response.json(), indent=4))
    return response.json()


def get_objects(data):
    return {t["name"]: t for t in data["data"]["__schema"]["types"]}


def parse_object(type_name, types, *, required):
    type_data = types[type_name]
    fields = {}
    for field in types[type_data["name"]]["fields"]:
        args = {}
        for arg in field["args"]:
            arg_type = parse_field(arg["type"], types, required=False)
            if isinstance(arg_type, ScalarType):
                args[arg["name"]] = Arg(scalar_type=arg_type)
                continue
            if isinstance(arg_type, ListType):
                args[arg["name"]] = Arg(list_type=arg_type)
                continue
            if isinstance(arg_type, ObjectType):
                args[arg["name"]] = Arg(object_type=arg_type)
                continue
            if isinstance(arg_type, EnumType):
                args[arg["name"]] = Arg(enum_type=arg_type)
                continue
            raise AssertionError(f"Unknown arg type: {type(arg_type)}, {arg_type}")

        field_type = parse_field(field["type"], types, required=False)

        if isinstance(field_type, ScalarType):
            fields[field["name"]] = Field(scalar_type=field_type, args=args)
            continue
        if isinstance(field_type, ListType):
            fields[field["name"]] = Field(list_type=field_type, args=args)
            continue
        if isinstance(field_type, ObjectType):
            fields[field["name"]] = Field(object_type=field_type, args=args)
            continue
        if isinstance(field_type, EnumType):
            fields[field["name"]] = Field(enum_type=field_type, args=args)
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

    if field_data["kind"] == "ENUM":
        return EnumType(
            name=field_data["name"],
            required=required,
            values=[
                enum_value["name"] for enum_value in types[field_data["name"]]["enumValues"]
            ],
        )

    raise AssertionError(f"Unknown field type. field_data: {field_data}")


if __name__ == "__main__":
    main()

# TODO: add descriptions
