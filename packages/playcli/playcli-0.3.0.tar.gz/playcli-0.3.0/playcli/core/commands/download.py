from rich import print

from playcli.models import Driver, Link


def call(id: str, driver: Driver):
    links: list[Link] = driver.download(id)

    if not links:
        print("[red]The game was not found[/]")

        return

    for link in links:
        print(f"[green bold]{link.target}:[/]")
        print(link.url)
