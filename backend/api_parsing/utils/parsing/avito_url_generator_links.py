from typing import List


class AvitoURLGenerator:
    agent: bool = False
    sort: bool = False

    AVITO_BASE_URL = ('https://www.avito.ru/'
                      'all/doma_dachi_kottedzhi/prodam/dom-ASgBAQICAUSUA9AQAUDYCBTOWQ'
                      '?f=ASgBAQECAUSUA9AQAkDYCBTOWY7eDhQCBEWSCBV7ImZy'
                      'b20iOjUwLCJ0byI6bnVsbH2WCBV7ImZyb20iOjEwLCJ0byI6bnVsbH3Gmgw')

    PRICE_RANGES = ['WeyJmcm9tIjowLCJ0byI6MzUwMDAwfeb6DhV7ImZyb20iOjEwLCJ0byI6bnVsbH0',
                    'beyJmcm9tIjozNTAwMDAsInRvIjo0NTAwMDB95voOFXsiZnJvbSI6MTAsInRvIjpudWxsfQ',
                    'beyJmcm9tIjo0NTAwMDAsInRvIjo1NTAwMDB95voOFXsiZnJvbSI6MTAsInRvIjpudWxsfQ',
                    'beyJmcm9tIjo1NTAwMDAsInRvIjo2NTAwMDB95voOFXsiZnJvbSI6MTAsInRvIjpudWxsfQ',
                    'beyJmcm9tIjo2NTAwMDAsInRvIjo3NTAwMDB95voOFXsiZnJvbSI6MTAsInRvIjpudWxsfQ',
                    'beyJmcm9tIjo4NTAwMDAsInRvIjo5NTAwMDB95voOFXsiZnJvbSI6MTAsInRvIjpudWxsfQ',
                    'ceyJmcm9tIjo5NTAwMDAsInRvIjoxMDAwMDAwfeb6DhV7ImZyb20iOjEwLCJ0byI6bnVsbH0',
                    'deyJmcm9tIjoxMDAwMDAwLCJ0byI6MTEwMDAwMH3m~g4VeyJmcm9tIjoxMCwidG8iOm51bGx9',
                    'deyJmcm9tIjoxMTAwMDAwLCJ0byI6MTI1MDAwMH3m~g4VeyJmcm9tIjoxMCwidG8iOm51bGx9',
                    'deyJmcm9tIjoxMjUwMDAwLCJ0byI6MTUwMDAwMH3m~g4VeyJmcm9tIjoxMCwidG8iOm51bGx9',
                    'deyJmcm9tIjoxNTAwMDAwLCJ0byI6MTc1MDAwMH3m~g4VeyJmcm9tIjoxMCwidG8iOm51bGx9',
                    'deyJmcm9tIjoxNzUwMDAwLCJ0byI6MjAwMDAwMH3m~g4VeyJmcm9tIjoxMCwidG8iOm51bGx9',
                    'deyJmcm9tIjoyMDAwMDAwLCJ0byI6MjUwMDAwMH3m~g4VeyJmcm9tIjoxMCwidG8iOm51bGx9',
                    'deyJmcm9tIjoyNTAwMDAwLCJ0byI6MzAwMDAwMH3m~g4VeyJmcm9tIjoxMCwidG8iOm51bGx9']

    def __init__(self, agent=None, sort=None):
        """
         Генератор URL-ссылок для парсинга Avito объявлений.
        Этот класс предоставляет методы для создания URL-ссылок на Avito с различными диапазонами цен.

        :param agent: Boolean агентские объявления
        :param sort: boolean сортировать по дате
        """
        if agent is not None:
            self.agent = agent
        if sort is not None:
            self.sort = sort

    def __generate_avito_url(self, price_range: str) -> str:
        """ Генерирует URL-ссылку на Avito объявления с указанным диапазоном цен.

                Args:
                    price_range (str): Диапазон цен в виде строки.

                Returns:
                    str: Сгенерированная URL-ссылка.
                    :param price_range: Фильтр по цене
        """
        return f"{self.AVITO_BASE_URL}{price_range}{'&s=104' if self.sort else ''}{'&user=1' if self.agent else ''}"

    def generate_all_urls(self) -> List[str]:
        """Генерирует список URL-ссылок на Avito объявления с различными диапазонами цен.

                Returns:
                    List[str]: Список сгенерированных URL-ссылок.
        """
        return [self.__generate_avito_url(price_range) for price_range in
                self.PRICE_RANGES]


urls = AvitoURLGenerator().generate_all_urls()

