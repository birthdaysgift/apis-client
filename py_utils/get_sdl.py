"""This script allows you to get SDL from existing api via http."""

import requests
from graphql import get_introspection_query, build_client_schema, print_schema


GRAPHQL_ENDPOINT = "https://rickandmortyapi.com/graphql"

response = requests.post(
    GRAPHQL_ENDPOINT,
    json={'query': get_introspection_query()},
    headers={'Content-Type': 'application/json'}
)

introspection_data = response.json()['data']
schema = build_client_schema(introspection_data)

sdl = print_schema(schema)

print(sdl)

with open("schema.graphql", "w") as f:
    f.write(sdl)
