from datetime import datetime
import re

from bs4 import BeautifulSoup

MONTH_MAP = {
    "Janeiro": 1,
    "Fevereiro": 2,
    "Março": 3,
    "Abril": 4,
    "Maio": 5,
    "Junho": 6,
    "Julho": 7,
    "Agosto": 8,
    "Setembro": 9,
    "Outubro": 10,
    "Novembro": 11,
    "Dezembro": 12,
}


class AttendencyParser:
    def __init__(self, html: str) -> None:
        self._html = html

    def history(self) -> list[dict]:
        history = []
        soup = BeautifulSoup(self._html, "html.parser")
        table = soup.find_all("table")[2].find_all("table")[-1]
        rows = table.find_all("tr")
        for row in rows[1:]:
            cols = row.find_all("td")
            data = [ele.text.strip() for ele in cols]
            year = int(data[0])
            month = MONTH_MAP[data[1]]
            date_asked = datetime.strptime(data[2], "%d/%m/%Y%H:%M")
            date_confirmed = re.sub(r"[^[0-9:/]]*", "", data[3])
            if date_confirmed == "":
                date_confirmed = None
            else:
                date_confirmed = datetime.strptime(date_confirmed, "%d/%m/%Y%H:%M")
            history.append(
                {
                    "year": year,
                    "month": month,
                    "asked": date_asked,
                    "confirmed": date_confirmed,
                }
            )
        return history

    def availability(self) -> bool:
        return "Opção não disponível" not in self._html
