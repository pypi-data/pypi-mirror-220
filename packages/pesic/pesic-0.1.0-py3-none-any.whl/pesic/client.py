import aiohttp
import asyncio
import logging
import os
from .custom_exceptions import MissingArgumentError, TokenError, CredentialsError

_LOGGER = logging.getLogger(__name__)

class RestClient:
    def __init__(self, base_url: str = None, username: str = None, password: str = None) -> None:
        self.retry_count = 0
        self.retry_threshold = 3
        if username is None or password is None:
            raise MissingArgumentError('Username and Password must be supplied')
        self.username = username
        self.password = password
        if base_url is None:
            # Mobile App uses https://ikus.pesc.ru/ikus4 endpoint
            self.base_url = 'https://ikus.pesc.ru/api'

        self.token = asyncio.run(self._fetch_token())

    async def _fetch_token(self) -> str:
        headers = {'Accept': 'application/json, text/plain, */*', 'Captcha': 'none','Content-Type': 'application/json',}
        data = {'type': 'PHONE', 'login': self.username, 'password': self.password,}
        url = f"{self.base_url}/v6/users/auth"
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=data) as response:
                token = await response.json()
                if type(token) == dict and token.get('code') == '3':
                    raise CredentialsError("Wrong username or password")
                else:
                    return token.get('auth')

    async def get(self, endpoint):
        _LOGGER.debug(f"GET request: {endpoint}")
        headers={"Authorization": f"Bearer {self.token}"}
        url = f"{self.base_url}{endpoint}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                result = await response.json()
                _LOGGER.debug(f"{endpoint} result: {result}")
                return result

    async def post(self, endpoint, data):
        _LOGGER.debug(f"POST request: {endpoint} with payload: {data}")
        headers = {
                'accept-encoding': 'gzip',
                'Authorization': 'Bearer ' + self.token,
                'content-type': 'application/json'
        }
        url = f"{self.base_url}{endpoint}"
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=data) as response:
                result = await response.json()
                _LOGGER.debug(f"{endpoint} result: {result}")
                return result
