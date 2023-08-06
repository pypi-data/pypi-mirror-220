from dataclasses import dataclass
from datetime import datetime
from typing import Callable, Awaitable
import logging

logger = logging.getLogger(__name__)


@dataclass
class AttendencyHistoryEntry:
    year: int
    month: int
    asked: datetime
    confirmed: datetime | None


class AttendencyHistory(list[AttendencyHistoryEntry]):
    def __str__(self) -> str:
        out: list[str] = []
        for entry in self:
            e = [entry.year, entry.month, entry.asked, entry.confirmed]
            out.append("\t".join(map(str, e)))
        return "\n".join(out)


class AttendencyPage:
    def __init__(
        self,
        history: AttendencyHistory,
        confirmation_callback: Callable[[], Awaitable[str]],
        available: bool,
    ):
        self._history = history
        self._available = available
        self.confirmation_callback = confirmation_callback

    def history(self) -> AttendencyHistory:
        return self._history

    def is_available(self):
        return self._available

    async def confirm(self) -> None:
        if self.is_available():
            logger.info("Requesting attendency confirmation...")
            await self.confirmation_callback()
