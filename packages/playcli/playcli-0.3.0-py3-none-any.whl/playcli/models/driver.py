class Link:
    def __init__(self, target: str, url: str) -> None:
        self.target: str = target
        self.url: str = url


class GameSearch:
    def __init__(self, id: str, platform: str, title: str) -> None:
        self.id: str = id
        self.title: str = title

        self.platform: str = platform


class Driver:
    url: str

    E: dict[str, dict]

    def download(self, id: str) -> list[Link]:
        ...

    def search(self, q: str, page: int) -> list[GameSearch]:
        ...
