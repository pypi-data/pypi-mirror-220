import uvloop

from shrt.database import init_engine
from . import url
from .base import AsyncTyper

cli = AsyncTyper()
cli.add_typer(url.app, name='url')

uvloop.install()


@cli.command()
async def init_db():
    await init_engine(apply_schema=True)
