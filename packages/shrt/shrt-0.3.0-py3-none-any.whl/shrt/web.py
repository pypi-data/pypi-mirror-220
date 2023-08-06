from .app import app, settings
from .database import engine, init_engine
from .utils import redis_disconnect, redis_init
from .views import redirect, status

app.include_router(status.router, prefix='/status', include_in_schema=False)
app.include_router(redirect.router, prefix='', tags=['redirect'], include_in_schema=True)


@app.on_event("startup")
async def startup():
    await init_engine()
    if settings.use_cache:
        redis_init(url=settings.redis_url)


@app.on_event("shutdown")
async def shutdown():
    await engine.dispose()
    if settings.use_cache:
        await redis_disconnect()
