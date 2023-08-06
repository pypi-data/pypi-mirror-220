from typing import AsyncGenerator, Callable

from sqlalchemy import Index, MetaData
from sqlalchemy.ext.asyncio import AsyncAttrs, AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, mapped_column

from .settings import get_global_settings

metadata = MetaData()
settings = get_global_settings()
engine: AsyncEngine | None = None
async_session: Callable[[], AsyncSession] | None = None


class Base(AsyncAttrs, DeclarativeBase):
    pass


class Redirects(Base):
    __tablename__ = 'redirect'

    id: Mapped[int] = mapped_column(primary_key=True)
    path: Mapped[str] = mapped_column(unique=True)
    target: Mapped[str]
    is_custom: Mapped[bool] = mapped_column(default=False)

    @declared_attr
    def __table_args__(cls):
        return (
            Index("custom_targets", "target", "is_custom"),
        )


async def init_engine(apply_schema: bool = False):
    global engine, async_session
    if not engine:
        connect_args = {}
        if 'sqlite' in settings.database_url.scheme:
            connect_args = {'check_same_thread': False}
        engine = create_async_engine(str(settings.database_url), connect_args=connect_args)
        if apply_schema:
            async with engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
    if not async_session:
        async_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session
