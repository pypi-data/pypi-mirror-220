from bs4 import BeautifulSoup
from typer import Exit

from playcli.core.web import scrap
from playcli.models.driver import Driver, GameSearch, Link


class Steamunlocked(Driver):
    url: str = "https://steamunlocked.net/"

    E: dict[str, dict] = {
        "game": {"link": ".btn-download"},
        "search": {"card": ".cover-item-title > a"},
    }

    def download(self, id: str) -> list[Link]:
        E: dict[str, str] = self.E["game"]

        try:
            parse: BeautifulSoup = scrap(self.url, [id], ex=False)

            link: Link = Link(
                target="DOWNLOAD", url=parse.select_one(E["link"])["href"]  # type: ignore
            )

            return [link]
        except Exit:
            return []

    def search(self, q: str, page: int) -> list[GameSearch]:
        E: dict[str, str] = self.E["search"]
        parse: BeautifulSoup = scrap(self.url, ["page", str(page)], {"s": q})

        rs: list[GameSearch] = []

        for el in parse.select(E["card"]):
            id: str = el["href"]  # type: ignore

            title: str = el.text.replace("Free Download", "")

            for x in [self.url, "-free-download", "/"]:
                id = id.replace(x, "")

            rs.append(
                GameSearch(id=id, title=title.strip(), platform=self.__class__.__name__)
            )

        return rs
