import typer
from rich import print

from app.core.config import get_settings

from .episode import episode

cli = typer.Typer(name="got", add_completion=False)
cli.add_typer(episode, name="episode")


@cli.command()
def settings():
    settings = get_settings()
    print(settings.dict())
