from bs4 import BeautifulSoup
import re

from .web_driver_current import WebDriverCurrent


class Parsing:
    number_page: int = 1
    count_page: int = None
    _html_page: BeautifulSoup = None

    def __init__(self, url: str, num_page: int):
        """
        Загрузка данных страницы Недвижимости из Авито

        :param url: адрес url страницы с объявлениями
        :param num_page: номер текущей страницы
        """
        self.count_page = self.get_count_pages(self.get_src_page(link=url))
        if num_page <= self.count_page:
            self._html_page = self.get_src_page(link=url, number_page=num_page)

    def get_count_pages(self, html: BeautifulSoup) -> int | None:
        """Получить количество страниц"""
        next_page_button = html.find("a", {"data-marker": "pagination-button/nextPage"})

        if next_page_button is not None:
            count_pages = next_page_button.previous_element.previous_element
            if count_pages is not None:
                return int(count_pages)

    def get_src_page(self, link: str, number_page: int = 1) -> BeautifulSoup:
        return WebDriverCurrent().get_source_page(url=link, num_page=number_page)

    def get_ads_link_data(self) -> list:
        """Формирование данных страницы"""
        # получить список блоков
        list_ads = self._get_list_ads_data(self._html_page)
        # получить dataset
        dataset = self._get_dataset(list_ads)
        return dataset

    def _get_list_ads_data(self, html):
        """Получить список блоков содержащих объявления"""
        return html.find_all("div", class_=re.compile("iva-item-content"))

    def _get_dataset(self, list_ads):
        dataset = []
        for ads in list_ads:
            video = self._check_ads_video(ads)
            link = self._get_link_to_ads(ads)
            price = self._get_price_to_ads(ads)
            title = self._get_title_ads(ads)
            link_img = self._get_link_img_ads(ads)

            item_data: dict = {
                "title": title,
                "link": link,
                "price": int(price),
                "is_video": video,
                "link_img": link_img,
            }
            dataset.append(item_data)
        return dataset

    def _check_ads_video(self, ads_source) -> bool | None:
        return ads_source.find("i", class_=re.compile("index-video")) is not None

    def _get_link_to_ads(self, ads):
        return "https://www.avito.ru" + ads.find(
            "a", class_=re.compile("iva-item-sliderLink")
        ).get("href")

    def _get_price_to_ads(self, ads):
        return ads.find("meta", itemprop="price").get("content")

    def _get_title_ads(self, ads):
        title = ads.h3.string
        return title.replace("\xa0", " ")

    def _get_link_img_ads(self, ads):
        _link = ads.find("li", class_=re.compile("photo-slider-list-item-"))
        if _link is not None:
            link = _link.get("data-marker")
            return link.split("slider-image/image-")[1]
