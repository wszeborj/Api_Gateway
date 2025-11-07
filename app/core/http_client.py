from typing import Any
import httpx


class HttpClient:
    def __init__(self, base_url: str) -> None:
        self.base_url: str = base_url

    async def request(self, method: str, path: str, **kwargs: Any) -> Any:
        async with httpx.AsyncClient(base_url=self.base_url) as client:
            response: httpx.Response = await client.request(method, path, **kwargs)
            response.raise_for_status()
            return response.json()
