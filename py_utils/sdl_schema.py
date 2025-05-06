from __future__ import annotations

from enum import Enum

from pydantic import BaseModel


class ObjectType(BaseModel):
    name: str
    fields: list[Field]


class Field(BaseModel):
    name: str
    type_: Type


class Type(BaseModel):
    kind: Kind
    required: bool

    scalar_type: ScalarType | None = None
    object_type: ObjectType | None = None
    list_type: Type | None = None


class Kind(Enum):
    SCALAR = "SCALAR"
    OBJECT = "OBJECT"
    LIST = "LIST"


class ScalarType(Enum):
    BOOLEAN = "BOOLEAN"
    FLOAT = "FLOAT"
    ID = "ID"
    INT = "INT"
    STRING = "STRING"


def main():
    result = ObjectType.model_validate({
        "name": "Query",
        "fields": [
            {
                "name": "username",
                "type_": {
                    "kind": "SCALAR",
                    "required": True,
                    "scalar_type": "STRING",
                },
            },
            {
                "name": "friends",
                "type_": {
                    "kind": "LIST",
                    "required": False,
                    "list_type": {
                        "kind": "OBJECT",
                        "required": True,
                        "object_type": {
                            "name": "User",
                            "fields": [
                                {
                                    "name": "username",
                                    "type_": {
                                        "kind": "SCALAR",
                                        "required": True,
                                        "scalar_type": "STRING",
                                    }
                                }
                            ]
                        }
                    }
                }
            }
        ]
    })

    print(result.model_dump_json())


if __name__ == "__main__":
    main()
