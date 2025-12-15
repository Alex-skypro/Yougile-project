# pages/base_page.py
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import allure
from config.settings import settings


class BasePage:
    """Базовый класс для всех Page Object."""

    def __init__(self, driver: WebDriver, timeout: int = 10):
        self.driver = driver
        self.base_url = settings.BASE_URL
        self.wait = WebDriverWait(driver, timeout)

    @allure.step("Открыть страницу {url}")
    def open(self, url: str = "") -> None:
        """Открыть указанный URL или базовый."""
        full_url = f"{self.base_url}{url}"
        self.driver.get(full_url)

    @allure.step("Найти элемент {locator}")
    def find_element(self, locator: tuple, timeout: int = None) -> WebElement:
        """Найти один элемент с ожиданием."""
        wait = self.wait if timeout is None else WebDriverWait(self.driver, timeout)
        return wait.until(EC.visibility_of_element_located(locator))

    @allure.step("Сделать скриншот")
    def take_screenshot(self, name: str = "screenshot") -> None:
        """Сделать скриншот и прикрепить к отчёту Allure."""
        from utils.attach import add_screenshot
        add_screenshot(self.driver, name)