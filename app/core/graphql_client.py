from typing import Any

from .http_client import HttpClient


class GraphQLClient:

    def __init__(self, base_url: str) -> None:

        self.http_client = HttpClient(base_url)
        self.graphql_endpoint = "/graphql"

    async def query(self, query: str, variables: dict[str, Any] | None = None) -> Any:
        payload = {
            "query": query,
            "variables": variables or {},
        }

        response = await self.http_client.request(
            "POST",
            self.graphql_endpoint,
            json=payload,
        )

        if "errors" in response:
            raise Exception(f"GraphQL errors: {response['errors']}")

        return response.get("data", {})
