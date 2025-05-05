import json
from pathlib import Path

import requests


def main():
    data = get_schema_json("http://localhost:5000/graphql")
    types = extract_types(data)
    for main_type in ("Query", "Mutation", "Subscription"):
        query_type = types.get(main_type)
        if query_type is None:
            continue
        print(f"{main_type}:")
        parse_fields(query_type["fields"], types, indent=1)


def get_schema_json(source):
    introspection_query_body = {
        "operationName":"IntrospectionQuery",
        "query": """
             query IntrospectionQuery {__schema {
                queryType { name }
                mutationType { name }
                subscriptionType { name }
                types {
                  ...FullType
                }
                directives {
                  name
                  description

                  locations
                  args(includeDeprecated: true) {
                    ...InputValue
                  }
                }
              }
            }

            fragment FullType on __Type {
              kind
              name
              description

              fields(includeDeprecated: true) {
                name
                description
                args(includeDeprecated: true) {
                  ...InputValue
                }
                type {
                  ...TypeRef
                }
                isDeprecated
                deprecationReason
              }
              inputFields(includeDeprecated: true) {
                ...InputValue
              }
              interfaces {
                ...TypeRef
              }
              enumValues(includeDeprecated: true) {
                name
                description
                isDeprecated
                deprecationReason
              }
              possibleTypes {
                ...TypeRef
              }
            }

            fragment InputValue on __InputValue {
              name
              description
              type { ...TypeRef }
              defaultValue
              isDeprecated
              deprecationReason
            }

            fragment TypeRef on __Type {
              kind
              name
              ofType {
                kind
                name
                ofType {
                  kind
                  name
                  ofType {
                    kind
                    name
                    ofType {
                      kind
                      name
                      ofType {
                        kind
                        name
                        ofType {
                          kind
                          name
                          ofType {
                            kind
                            name
                          }
                        }
                      }
                    }
                  }
                }
              }
            }
        """
    }
    response = requests.post(source, json=introspection_query_body)
    print(response.status_code)
    return response.json()


def extract_types(data):
    return {t["name"]: t for t in data["data"]["__schema"]["types"]}


def parse_fields(fields, types, indent=0):
    for field in fields:
        description = field.get("description")
        if description:
            print(f"{'    '*indent}// {oneline(description)}")

        # raise Exception(
        #     "TODO: add handling for NON_NULL type modificator, "
        #     "comment this exception if you want to get current functionality"
        # )

        type_ = field["type"]
        type_name = field["type"]["name"]
        if type_["kind"] == "LIST":
            type_name = f"[{type_['ofType']['name']}]"
            print(f"{'    '*indent}{field['name']}: {type_name}")
            print()
            continue

        print(f"{'    '*indent}{field['name']}: {type_name}")
        print()

        if type_["kind"] == "OBJECT" and type_["name"] in types:
            indent += 1
            parse_fields(types[type_['name']]["fields"], types, indent)
            indent -= 1

def oneline(text):
    return " ".join(text.split("\n")) if "\n" in text else text


if __name__ == "__main__":
    main()

