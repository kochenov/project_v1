from starlette.responses import JSONResponse

from .avito_url_generator_links import AvitoURLGenerator
from .parsing import Parsing
from modules.parsing_process.repository import ProcessParsingRepository
from modules.links.repository import LinkRepository


class Process:
    """
    Класс для запуска процесса парсинга страниц Авито.


    Атрибуты:
        sort (bool): Включение сортировки
        agent (bool): Включение к выдачи агенств
        _list_urls (list): Список URL-ов для обработки.
        _current_iterate (int): Текущая итерация обработки.
        _current_page (int): Текущая страница обработки.
        _error (bool): Флаг ошибки в процессе обработки.

    Алгоритм:
         1. Инициализация, получение списка ссылок для работы
         2.
         3.
         4.
         5.
         6.
    """

    sort: bool
    agent: bool
    _list_urls: list
    _current_iterate: int = 0
    _current_page: int = 1
    _error: bool = False

    # инициализация класса
    def __init__(self, sort: bool, agent: bool):
        """
        Запуск процесса парсинга страниц Авито.

        :param sort: Сортировка
        :param agent: Агентства
        """
        self.sort = sort
        self.agent = agent

        self._list_urls = self.__get_parsing_links()

    def __get_parsing_links(self) -> list:
        """
        :return (list): список ссылок для парсинга
        """
        return AvitoURLGenerator(sort=self.sort, agent=self.agent).generate_all_urls()

    async def run(self) -> JSONResponse | bool:
        """
        Запуск процесса получения данных объявлений
        """
        try:
            # 1 - получение данных и инициализация значений
            await self._get_record_last()
            # 2 - старт парсинга
            await self._start_parsing_lists_ads(self._list_urls[self._current_iterate])
            return JSONResponse({"task": "выполнен"})
        except Exception as e:
            print(e)
            return False

    async def _get_record_last(self) -> None:
        """
        Метод получает последнюю запись о процессе
        парсинга из базы данных и инициализирует свойства
        класса
        """
        # получить последнюю запись из БД
        record_item_process = await ProcessParsingRepository.find_last()

        # если в БД есть запись
        # присваиваю данные атрибутам объекта
        # если записи ещё нет, значения остаются по умолчанию
        if record_item_process is not None:
            self._init_property(
                iterate=record_item_process.iterate,
                page=record_item_process.page,
                error=record_item_process.error,
            )

    def _init_property(self, iterate: int, page: int, error: bool) -> None:
        """Инициализация свойств объекта"""
        self._current_iterate = iterate
        self._current_page = (
            page + 1 if not error else page
        )  # если есть ошибка оставим как есть
        self._error = error
        if error:
            print(
                f"\nВ последней записи есть ошибка:\nУстанавливаю: \n    Итерация [{self._current_iterate}]\n    "
                f"Страница [{self._current_page}]"
            )

    async def _start_parsing_lists_ads(self, link: str):
        """
        Старт парсинга страницы
        :param link: ссылка для парсинга
        :return:
        """
        try:
            print("Процесс парсинга запущен")

            parsing = Parsing(url=link, num_page=self._current_page)
            # 1. узнаём количество страниц
            count_pages = parsing.count_page
            # 2. Если число текущей страница больше общего количества страниц
            if self._current_page > count_pages:
                # увеличиваем итерацию
                if self._current_iterate + 1 > len(self._list_urls):
                    self._current_iterate = 0
                else:
                    self._current_iterate += 1
                # скидываем текущую страницу
                self._current_page = 1
                # сохраняем
                await ProcessParsingRepository.add(
                    iterate=self._current_iterate, page=self._current_page, error=True
                )
                return
            # Получить данные о ссылке
            link_data = parsing.get_ads_link_data()
            # если пусто есть ошибка (True)
            self._error = not len(link_data)
            # сохранить ссылку
            for item in link_data:
                existing_link = await LinkRepository.find_one_or_none(link=item["link"])
                if existing_link is None:
                    await LinkRepository.add(
                        link=item["link"],
                        price=item["price"],
                        title=item["title"],
                        is_video=item["is_video"],
                        link_img=item["link_img"],
                    )

            await ProcessParsingRepository.add(
                iterate=self._current_iterate,
                page=self._current_page,
                error=self._error,
            )
            print("Процесс парсинга успешно окончен")
            return True
        except Exception as e:
            await ProcessParsingRepository.add(
                iterate=self._current_iterate, page=self._current_page, error=True
            )
            raise Exception(f"Не удалось сделать парсинг страницы / {e}")
