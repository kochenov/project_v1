from fastapi import APIRouter, BackgroundTasks, Query, Depends, HTTPException
from fastapi_pagination import Page, paginate
from fastapi_pagination.utils import disable_installed_extensions_check

from modules.links.repository import LinkRepository
from modules.links.schemas import ReadLinkSchema

router = APIRouter(prefix="/links", tags=["Ссылки парсинга"])
disable_installed_extensions_check()


@router.get("/list", name="Список ссылок для парсинга")
# @cache(expire=10)
async def get_links(
    is_video: bool = Query(False, description="Наличие видео обзора"),
) -> Page[ReadLinkSchema]:
    """
    Получить список ссылок для парсинга.
    """
    try:
        links = await LinkRepository.find_all(is_video=is_video)
        return paginate(links)
    except Exception as e:
        print(e)
