from dataclasses import dataclass
from datetime import datetime
import logging

from ppgee.parser import parse_frequency_history

logger = logging.getLogger(__name__)


@dataclass
class HistoryEntry:
    year: int
    month: int
    asked: datetime
    confirmed: datetime | None


class History(list[HistoryEntry]):
    def __str__(self) -> str:
        out: list[str] = []
        for entry in self:
            e = [entry.year, entry.month, entry.asked, entry.confirmed]
            out.append("\t".join(map(str, e)))
        return "\n".join(out)


class FrequencyPage:
    def __init__(self, html, confirmation_callback):
        self.html = html
        self._history = History()
        self.confirmation_callback = confirmation_callback

    def _build_history(self):
        result_list = parse_frequency_history(self.html)
        for item in result_list:
            self._history.append(HistoryEntry(**item))

    def history(self) -> History:
        if not self._history:
            self._build_history()
        return self._history

    def is_available(self):
        if "Opção não disponível" in self.html:
            return False
        return True

    async def confirm(self) -> None:
        if self.is_available():
            logger.info("Requesting frequency confirmation...")
            await self.confirmation_callback()
