from fastapi import APIRouter, BackgroundTasks
from fastapi_pagination.utils import disable_installed_extensions_check

from core.config import settings
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
