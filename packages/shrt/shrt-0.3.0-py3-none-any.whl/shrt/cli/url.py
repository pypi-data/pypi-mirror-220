import typer
from pydantic import ValidationError
from sqlalchemy import delete, select
from sqlalchemy.exc import IntegrityError
from tabulate import tabulate

from shrt import database
from shrt.app import settings
from shrt.database import Redirects
from shrt.schemas import Redirect, RedirectIn
from shrt.utils import random_path
from .base import AsyncTyper

app = AsyncTyper()


@app.callback()
async def url_callback():
    await database.init_engine()


@app.command(name='add')
async def cmd_add(target: str, path: str = None, create_new: bool = False):
    is_custom = bool(path)
    if not path:
        path = random_path(settings.default_random_length)

    # Short-circuit if target is already shortened, and we are not forced to create a new one
    if not create_new:
        async with database.async_session() as session:
            result = await session.execute(
                select(Redirects).where(Redirects.target == target).order_by(
                    Redirects.is_custom,
                    Redirects.id.desc(),
                )
            )
            optional_redirect = result.scalar_one_or_none()
            if optional_redirect:
                redirect = Redirect.model_validate(optional_redirect)
                typer.echo('URL is already shortened')
                typer.echo(tabulate([redirect.model_dump()], headers='keys'))
                raise typer.Exit()

    try:
        redirect_in = RedirectIn(
            path=path,
            target=target,
            is_custom=is_custom,
        )
    except ValidationError as e:
        typer.echo(e, err=True)
        raise typer.Exit(code=1)

    if not redirect_in.target.path:
        redirect_in.target.join('/')

    async with database.async_session() as session:
        instance = Redirects(**redirect_in.model_dump(mode="json"))
        try:
            session.add(instance)
            await session.commit()
        except IntegrityError:
            typer.echo('A Shortened URL with this path already exists', err=True)
            raise typer.Exit(code=1)
        redirect = Redirect(**redirect_in.model_dump(), id=instance.id)
        typer.echo(tabulate([redirect.model_dump()], headers='keys'))


@app.command(name='list')
async def cmd_list():
    async with database.async_session() as session:
        result = await session.execute(select(Redirects))
        result_set = [Redirect.model_validate(r).model_dump() for r in result.scalars()]
        typer.echo(tabulate(result_set, headers='keys'))


@app.command(name='get')
async def cmd_get(path: str):
    async with database.async_session() as session:
        result = await session.execute(select(Redirects).where(Redirects.path == path))
        redirect = result.scalar_one_or_none()
        if not redirect:
            typer.echo(f'No URL found for path "{path}"', err=True)
            raise typer.Exit(code=1)
        result_set = [Redirect.model_validate(redirect).model_dump()]
        typer.echo(tabulate(result_set, headers='keys'))


@app.command(name='delete')
async def cmd_delete(path: str):
    async with database.async_session() as session:
        result = await session.execute(delete(Redirects).where(Redirects.path == path))
        if not result.rowcount:
            typer.echo(f'No URL found for path "{path}"', err=True)
            raise typer.Exit(code=1)
        await session.commit()
        typer.echo(f'Deleted redirect for path "{path}"')
