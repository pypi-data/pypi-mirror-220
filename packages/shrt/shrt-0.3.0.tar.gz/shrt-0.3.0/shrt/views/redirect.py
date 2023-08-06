from fastapi import APIRouter, Depends
from fastapi.responses import PlainTextResponse, RedirectResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from shrt.app import settings
from shrt.database import Redirects, get_async_session
from shrt.schemas import Redirect
from shrt.utils import get_cache, set_cache

router = APIRouter()


@router.get('/{path}', response_class=RedirectResponse, status_code=302, responses={
    404: {'content': {'text/plain': {'default': 'Page not found'}}}
})
async def redirect(path: str, db: AsyncSession = Depends(get_async_session)):
    if settings.use_cache:
        cached_result = await get_cache(f'shrt:url:{path}')
        if cached_result:
            return cached_result
    query = await db.execute(select(Redirects).where(Redirects.path == path))
    result = query.scalar_one_or_none()
    if not result:
        return PlainTextResponse('Page not found', status_code=404)
    else:
        redirect_obj = Redirect.model_validate(result)
        if settings.use_cache:
            await set_cache(f'shrt:url:{path}', redirect_obj.target, ex=86400 * 365)
        return redirect_obj.target
