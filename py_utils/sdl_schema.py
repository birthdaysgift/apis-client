from __future__ import annotations

from enum import Enum

from pydantic import BaseModel


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
    BOOLEAN = "BOOLEAN"
    FLOAT = "FLOAT"
    ID = "ID"
    INT = "INT"
    STRING = "STRING"





def main():
    result = ObjectType.model_validate({
        "name": "Query",
        "required": True,
        "fields": [
            {
                "name": "username",
                "type_": {
                    "scalar_type": {
                        "required": True,
                        "name": "STRING",
                    },
                },
            },
            {
                "name": "friends",
                "type_": {
                    "list_type": {
                        "required": True,
                        "type_": {
                            "object_type": {
                                "required": True,
                                "name": "User",
                                "fields": [
                                    {
                                        "name": "username",
                                        "type_": {
                                            "scalar_type": {
                                                "name": "STRING",
                                                "required": True,
                                            },
                                        },
                                    },
                                    {
                                        "name": "age",
                                        "type_": {
                                            "scalar_type": {
                                                "name": "INT",
                                                "required": True,
                                            },
                                        },
                                    },
                                ],
                            },
                        },
                    },
                },
            },
        ],
    })

    print(result.model_dump_json())


if __name__ == "__main__":
    main()
