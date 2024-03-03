from bs4 import BeautifulSoup
import re

from .locations import HelperLocation
from .web_driver_current import WebDriverCurrent


class ParsingFull:
    _link = None
    _url: str  # HTML ссылка на объявление
    _title: str
    _price: int  # Цена на дом
    _area_house: int  # Площадь дома в квадратных метрах
    _land_area: int  # Площадь земельного участка в квадратных метрах
    _location: dict = None  # Местоположение участка и дома
    _distance_to_city: int = None  # Дистанция до центра города в километрах
    _year_of_construction: int = None  # Год постройки дома
    _wall_material: str = None  # Материал стен дома
    _bathroom: bool = False  # Наличие санузла в доме
    _electricity: bool = False  # Наличие электричества
    _gas: bool = False  # Наличие газа
    _heating: bool = False  # Наличие отопления
    _sewerage: bool = False  # Наличие канализации
    _video_url: str = None  # URL видео обзора дома
    _description: str = None  # Описание
    _image: str = None
    _room_count: int = None

    _data_source: dict = {}
    _source: BeautifulSoup

    def __init__(self, link):
        self._link = link
        self._url = link.link
        self._image = link.link_img if link.link_img else self._get_image()
        self._title = link.title if link.title else None
        self._price = link.price if link.price else None

    def _get_src_page(self, url: str):
        """Получить код страницы"""
        self._source = WebDriverCurrent().get_source_full_page(url)

    def run(self):
        self._get_src_page(self._url)
        self._get_area_house()
        self._get_land_area()
        self._get_location()
        self._get_distance_to_city()
        self._get_year_of_construction()
        self._get_wall_material()
        self._get_bathroom()
        self._get_communications()
        if self._link.is_video:
            self._get_video_url()
        self._get_room_count()

    def get_data(self) -> dict:
        self._data_source = {
            "url": self._url,
            "title": self._title,
            "price": self._price,
            "area_house": self._area_house,
            "land_area": self._land_area,
            "location": self._location,
            "distance_to_city": self._distance_to_city,
            "year_of_construction": self._year_of_construction,
            "wall_material": self._wall_material,
            "bathroom": self._bathroom,
            "electricity": self._electricity,
            "sewerage": self._sewerage,
            "heating": self._heating,
            "gas": self._gas,
            "image": self._image,
            "url_video": self._video_url,
        }
        return self._data_source

    def _get_area_house(self):
        """Получить площадь дома"""
        try:
            area_house = self._source.find(string="Площадь дома").parent.next_sibling
            self._area_house = int(float(area_house.text.split("\xa0")[0]))
        except Exception as e:
            print(f"Error [Не удалось получить площадь дома]: {e}")

    def _get_land_area(self):
        """Получить площадь участка"""
        try:
            land_area = self._source.find(string="Площадь участка").parent.next_sibling
            self._land_area = int(float(land_area.text.split("\xa0")[0]))
        except Exception as e:
            print(f"Error [Не удалось получить площадь участка]: {e}")

    def _get_location(self):
        """Получить адрес"""
        try:
            element = self._source.find("div", itemprop="address")
            location = element.find("span").text

            # self._location = location.split(", ")
            self._location = HelperLocation(location).location

        except Exception as e:
            print(f"Error [Не удалось получить площадь участка]: {e}")

    def _get_distance_to_city(self):
        """Расстояние до города"""
        try:
            distance_to_city = self._source.find(
                string="Расстояние до центра города"
            ).parent.next_sibling
            self._distance_to_city = int(distance_to_city.text.split("\xa0")[0])
        except Exception as e:
            print(f"Error [Не удалось получить расстояние до города]: {e}")

    def _get_year_of_construction(self):
        """Получить год постройки"""
        try:
            year_of_construction = self._source.find(string="Год постройки")
            if year_of_construction:
                self._year_of_construction = int(
                    year_of_construction.parent.next_sibling.text
                )
        except Exception as e:
            print(f"Error [Не удалось получить год постройки]: {e}")

    def _get_wall_material(self):
        """Получить материал дома"""
        try:
            wall_material = self._source.find(string="Материал стен")
            if wall_material:
                self._wall_material = wall_material.parent.next_sibling.text
        except Exception as e:
            print(f"Error [Не удалось получить информацию о материале дома]: {e}")

    def _get_bathroom(self):
        """Наличие санузла в доме"""
        try:
            bathroom = self._source.find(string="Санузел")
            if bathroom:
                if bathroom.parent.next_sibling.text == "в доме":
                    self._bathroom = True
        except Exception as e:
            print(f"Error [Не удалось получить информацию о материале дома]: {e}")

    def _get_communications(self):
        """Наличие электричества"""
        try:
            communications_el = self._source.find(string="Коммуникации")
            if communications_el:
                communications = communications_el.parent.next_sibling.text
                communications_list = communications.split(", ")
                for item in communications_list:
                    if item == "электричество":
                        self._electricity = True
                    if item == "канализация":
                        self._sewerage = True
                    if item == "отопление":
                        self._heating = True
                    if item == "газ":
                        self._gas = True

        except Exception as e:
            print(f"Error [Не удалось получить информацию о коммуникациях дома]: {e}")

    def _get_image(self):
        """Получить фото - image-frame-wrapper"""

        try:
            image_element = self._source.find(
                "div", class_=re.compile("image-frame-wrapper-")
            )
            image_url = image_element.find("img").get("src")
            self._image = image_url
        except Exception as e:
            print(f"Error [Не удалось получить стоимость]: {e}")

    def _get_video_url(self):
        try:
            source = WebDriverCurrent().get_video_element(self._url)
            # gallery-block-itemViewGallery
            gallery_element = source.find(
                "div", class_=re.compile("gallery-block-itemViewGallery")
            )
            video_url = gallery_element.find("iframe").get("src")
            # Разделение URL-адреса по '?'
            parts = video_url.split("?")

            # Извлечение части URL-адреса до '?'
            self._video_url = parts[0]
        except Exception as e:
            print(f"Error [Не удалось получить адрес видео]: {e}")

    def _get_room_count(self):
        """Количество комнат"""
        try:
            room_count = self._source.find(string="Количество комнат")
            if room_count:
                self._room_count = int(room_count.parent.next_sibling.text)
        except Exception as e:
            print(f"Error [Не удалось получить информацию о количестве комнат]: {e}")
