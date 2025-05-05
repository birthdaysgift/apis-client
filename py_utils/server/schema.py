import strawberry


@strawberry.type
class Query:
    version: int


schema = strawberry.Schema(query=Query)

