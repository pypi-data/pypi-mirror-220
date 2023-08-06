from bs4 import BeautifulSoup
from typer import Exit

from playcli.core.web import scrap
from playcli.models.driver import Driver, GameSearch, Link


class Elamigos(Driver):
    url: str = "https://www.elamigos-games.com/"

    E: dict[str, dict] = {
        "game": {"links": "#dw > a"},
        "search": {
            "card": ".card-title > a",
        },
    }

    def download(self, id: str) -> list[Link]:
        E: dict[str, str] = self.E["game"]

        try:
            parse: BeautifulSoup = scrap(self.url, ["games", id], ex=False)

            links: list[Link] = []

            for lk in parse.select(E["links"]):
                links.append(Link(target=lk.text, url=lk["href"]))  # type: ignore

            return links
        except Exit:
            return []

    def search(self, q: str, page: int) -> list[GameSearch]:
        E: dict[str, str] = self.E["search"]
        parse: BeautifulSoup = scrap(self.url, params={"q": q, "page": page})

        rs: list[GameSearch] = []

        for el in parse.select(E["card"]):
            if not el["href"].startswith(self.url):  # type: ignore
                continue

            title: str = el.text
            id: str = el["href"].replace(self.url + "games/", "")  # type: ignore

            rs.append(GameSearch(id=id, title=title, platform=self.__class__.__name__))

        return rs
