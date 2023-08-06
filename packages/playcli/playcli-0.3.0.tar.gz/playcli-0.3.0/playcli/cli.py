from typing import Annotated

from rich import print
from typer import Exit, Option, Typer

from playcli.core import commands as c
from playcli.models.platforms import Platforms

app: Typer = Typer(help="Download games with ease")


@app.command(help="Code repository")
def credits() -> None:
    c.credits()


@app.command(help="Search for games on multiple platforms")
def search(
    title: list[str],
    page: Annotated[int, Option("--page", "-p", min=1)] = 1,
    platform: Annotated[Platforms, Option()] = Platforms.RECURSIVE,
) -> None:
    c.search(" ".join(title), page, platform)


@app.command(help="Game download links")
def download(id: str) -> None:
    f_ = Platforms.ALL.find(id)

    if not f_:
        print("[red]This id is invalid, or does not have a registered platform.[/]")

        raise Exit(1)

    c.download(*f_)
