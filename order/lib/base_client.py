import httpx
from abc import ABC
from enum import Enum


class HTTPMethod(str, Enum):
    get = 'GET'
    post = 'POST'
    patch = 'PATCH'
    put = 'PUT'
    delete = 'DELETE'


class BaseClient(ABC):
    domain: str

    async def _make_request(
        self,
        url: str,
        method: HTTPMethod,
        params: dict = None,
        data: dict = None,
        headers: dict = None,
    ):
        async with httpx.AsyncClient() as client:
            response: httpx.Response = await client.request(
                method=method.value,
                url=self.domain + url,
                params=params,
                data=data,
                headers=headers,
            )
        return response
