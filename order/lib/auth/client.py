from fastapi import HTTPException
from order.lib import BaseClient, HTTPMethod
from order.config import settings


class AuthClient(BaseClient):
    domain = settings.AUTH_URL

    async def get_user_info(self, token: str) -> dict:
        headers = {'X-Token': token}
        response = await self._make_request(
            url='/info',
            method=HTTPMethod.get,
            headers=headers,
        )

        if response.status_code >= 400:
            detail = response.json()['detail']
            raise HTTPException(
                status_code=response.status_code,
                detail=detail,
            )

        user_info = response.json()
        return user_info
