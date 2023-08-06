from datetime import date
import logging

import aiohttp

from ppgee.errors import RequestException

URL_BASE = "https://www.ppgee.ufmg.br/ppgeenet"
logger = logging.getLogger(__name__)


class HttpClient:
    def __init__(self, session: aiohttp.ClientSession):
        self.session = session

    async def _request(self, method: str, url: str, **kwargs) -> str:
        async with self.session.request(method, url, **kwargs) as resp:
            logger.debug(f"Request: {url} Status: {resp.status}")
            if resp.status != 200:
                raise RequestException(
                    f"Request to url {url} with method {method} failed with status code {resp.status}."
                )
            return await resp.text()

    async def login(self, user: str, password: str) -> str:
        data: dict[str, str] = {"login": user, "senha": password}
        return await self._request("post", f"{URL_BASE}/login.php", data=data)

    async def attendency(self) -> str:
        return await self._request("get", f"{URL_BASE}/afreq.php")

    async def attendency_confirmation(self) -> str:
        today = date.today()
        data: dict[str, str] = {
            "freqano": str(today.year),
            "freqmes": str(today.month),
            "confirma": "checkbox",
        }
        return await self._request("POST", f"{URL_BASE}/afreqpasso2.php", data=data)

    async def logoff(self) -> str:
        return await self._request("get", f"{URL_BASE}/logoff.php")
