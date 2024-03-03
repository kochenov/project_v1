from fastapi import APIRouter, BackgroundTasks
from fastapi_pagination.utils import disable_installed_extensions_check

from core.config import settings
from modules.links.repository import LinkRepository
from utils.parsing.parsing_full_ads import ParsingFull
from utils.parsing.process import Process

router = APIRouter(prefix="/parsing", tags=["Парсинг объявлений"])
disable_installed_extensions_check()


@router.get("/start/{secret_code}", name="Запуск задачи")
async def start_task_parsing(secret_code: int, task: BackgroundTasks):
    if secret_code == settings.secret_parse:
        process = Process(sort=True, agent=False)
        task.add_task(process.run)
        return {"message": "Задача запущена"}
    else:
        return {"message": "Задача не запущена"}


@router.get("/run/{secret_code}/{link_id}", name="Запуск задачи парсинга")
async def start_task_parsing_ads(secret_code: int, link_id: int, task: BackgroundTasks):
    if secret_code == settings.secret_parse:
        link = await LinkRepository.find_one_or_none(id=link_id)
        if link:
            parsing = ParsingFull(link)
            task.add_task(parsing.run)
            # return parsing.get_data()
            return {"message": "Задача запущена"}
    else:
        return {"message": "Задача не запущена"}
