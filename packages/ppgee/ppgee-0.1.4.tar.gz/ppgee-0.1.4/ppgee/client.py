import logging

import aiohttp

from ppgee import errors
from ppgee.http import HttpClient
from ppgee.pages import AttendencyPage, AttendencyHistory, AttendencyHistoryEntry
from ppgee.parsers import AttendencyParser
from ppgee.permissions import is_logged_check

logger = logging.getLogger(__name__)


class PPGEE:
    def __init__(self, user: str | None = None, password: str | None = None) -> None:
        self.user = user
        self.password = password
        self.session: aiohttp.ClientSession
        self.http: HttpClient
        self.is_logged: bool = False

    async def start(self):
        self.session = aiohttp.ClientSession()
        self.http = HttpClient(self.session)

    async def close(self):
        if self.session:
            await self.session.close()

    async def __aenter__(self):
        await self.start()
        await self.login()
        return self

    async def __aexit__(self, *_) -> None:
        if self.is_logged:
            await self.logoff()
        await self.close()

    async def login(self) -> None:
        logger.info("Logging in...")
        if self.user and self.password:
            resp = await self.http.login(self.user, self.password)
            if "aindex" not in resp:  # authentication failed
                await self.close()
                raise errors.InvalidCredentialsException()
            self.is_logged = True
        else:
            logger.info("Logged in without credentials")

    @is_logged_check
    async def attendency(self) -> AttendencyPage:
        logger.info("Requesting attendency page...")
        html = await self.http.attendency()
        parser = AttendencyParser(html)
        history = AttendencyHistory(
            (AttendencyHistoryEntry(**item) for item in parser.history())
        )
        return AttendencyPage(
            history, self.http.attendency_confirmation, parser.availability()
        )

    @is_logged_check
    async def logoff(self) -> None:
        logger.info("Logging off...")
        self.is_logged = False
        await self.http.logoff()
