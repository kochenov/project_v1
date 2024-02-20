from fastapi import APIRouter, BackgroundTasks, Query, Depends, HTTPException
from fastapi_pagination import Page, paginate
from fastapi_pagination.utils import disable_installed_extensions_check

from .repository import LinkRepository
from .schemas import ReadLinkSchema, NewLinkSchema, UpdateLinkSchema

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


@router.patch("/edit/{link_id}", name="Обновить ссылку")
async def update_link(link_id: int, link_update: UpdateLinkSchema = Depends()):
    """
    Обновить данные ссылки по ID.
    """
    link = await LinkRepository.find_one_or_none(id=link_id)
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")

    await LinkRepository.update(link_id, **link_update.model_dump())
    return {"message": "Ссылка успешно обновлена"}


@router.post("/add", name="Добавление новой ссылки")
async def add_link(link_data: NewLinkSchema = Depends()) -> dict:
    """
    Создание новой записи об объявлении


    :param link_data: данные для записи
    :return: dict
    """
    try:
        # получаем ссылку из базы данных
        link = await LinkRepository.find_one_or_none(link=link_data.link)
        # если такая ссылка присутствует в БД
        if link:
            # выводим ошибку 500 с пояснением
            raise HTTPException(status_code=500, detail="Такая ссылка уже есть")
        # если ссылке в БД нет, то делаем новую запись
        await LinkRepository.add(**link_data.model_dump())
        return {"message": "Запись успешно создана", "error": None}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")
