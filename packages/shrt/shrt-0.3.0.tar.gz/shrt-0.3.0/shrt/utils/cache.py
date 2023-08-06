"""
Assuming here we are using Redis
Assuming connection pool is initiated by the server
"""
import asyncio

from pydantic import RedisDsn
try:
    from redis.asyncio import ConnectionPool, Redis
    redis_installed = True
except ImportError:
    redis_installed = False
    ConnectionPool, Redis = None, None

MAX_CLIENTS = 10000

redis_pool: ConnectionPool = None
redis_conn: Redis = None

# Allow some space for rogue connections, so we don't fail desired connections
_redis_semaphore = asyncio.Semaphore(int(MAX_CLIENTS * 0.9))


def redis_init(url: str | RedisDsn):
    if not redis_installed:
        return None
    global redis_pool, redis_conn
    if not redis_pool:
        redis_pool = ConnectionPool.from_url(url, max_connections=MAX_CLIENTS)
    if not redis_conn:
        redis_conn = Redis(connection_pool=redis_pool)


async def redis_disconnect():
    if not redis_installed:
        return None
    global redis_pool, redis_conn
    if redis_conn:
        await redis_conn.close()
        redis_conn = None
        redis_pool = None


async def get_cache(key: str) -> str | None:
    if not redis_installed:
        return None
    async with _redis_semaphore:
        return await redis_conn.get(key)


async def set_cache(key: str, value: str, **kwargs):
    if not redis_installed:
        return None
    async with _redis_semaphore:
        return await redis_conn.set(key, value, **kwargs)
