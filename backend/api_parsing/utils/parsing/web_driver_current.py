from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


class WebDriverCurrent:
    AVITO_BASE: str = 'https://www.avito.ru/'

    def __init__(self):
        self.options = self._get_default_options()

    def _get_default_options(self):
        options = webdriver.ChromeOptions()
        prefs = {"profile.managed_default_content_settings.images": 2}
        options.add_argument('--headless')
        options.add_argument('--disable-extensions')
        options.add_argument('--blink-settings=imagesEnabled=false')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-background-networking')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument("--log-level=3")  # fatal
        options.add_argument('--ignore-certificate-errors-spki-list')
        options.add_experimental_option("prefs", prefs)
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_argument("window-size=1920,1080")
        options.add_argument("--disable-extensions")
        options.add_argument("--proxy-server='direct://'")
        options.add_argument("--proxy-bypass-list=*")
        options.add_argument("--start-maximized")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-browser-side-navigation")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-features=site-per-process")
        options.add_argument("--enable-features=NetworkServiceInProcess")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-default-apps")
        options.add_argument("--disable-translate")
        return options

    def _get_driver(self):
        try:
            chrome = ChromeDriverManager().install()
            driver = webdriver.Chrome(service=ChromeService(chrome), options=self.options)
            return driver
        except Exception as e:
            print(f"An error occurred: {e}")

    def _add_cookie(self, driver, cookie=None):

        """ Куки для сеанса """
        try:
            if cookie is None:
                cookie = {"name": "view", "value": "gallery"}
            driver.get(self.AVITO_BASE)
            driver.add_cookie(cookie)
            return driver
        except Exception as e:
            print(e)

    def get_source_page(self, url, num_page: int):
        driver = None

        try:
            driver = self._add_cookie(self._get_driver())
            driver.get(f"{url}&p={num_page or 1}")
            source = driver.page_source
            return self._get_html(source)
        except Exception as e:
            print(f"{e}")
        finally:
            if driver is not None:
                driver.quit()

    def _get_html(self, source: str) -> BeautifulSoup:
        """ Получить содержимого в формате BS4 """
        return BeautifulSoup(source, 'html.parser')
