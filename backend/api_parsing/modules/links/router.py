from fastapi import APIRouter, BackgroundTasks, Query, Depends, HTTPException
from fastapi_pagination import Page, paginate
from fastapi_pagination.utils import disable_installed_extensions_check

from .repository import LinkRepository
from .schemas import ReadLinkSchema, NewLinkSchema

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


@router.post("/add", name="Добавление новой ссылки")
async def add_link(link_data: NewLinkSchema = Depends()):
    """
    Создание новой записи об объявлении
    """
    try:
        link = await LinkRepository.find_one_or_none(link=link_data.link)

        if link:
            raise HTTPException(status_code=500, detail="Такая ссылка уже есть")
        await LinkRepository.add(**link_data.model_dump())
        return {"message": "Запись успешно создана", "error": None}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")
