# tests/conftest.py
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from config.settings import settings


@pytest.fixture(scope="function")
def driver():
    """Фикстура для создания и закрытия браузера."""
    options = webdriver.ChromeOptions()
    if settings.HEADLESS:
        options.add_argument("--headless")
    options.add_argument("--window-size=1920,1080")

    # Менеджер сам скачает нужный chromedriver
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    driver.implicitly_wait(settings.IMPLICIT_WAIT)

    yield driver  # Отдаём драйвер тесту

    driver.quit()  # Закрываем после теста


@pytest.fixture
def login_page(driver):
    """Фикстура возвращает готовый экземпляр LoginPage."""
    from pages.login_page import LoginPage
    page = LoginPage(driver)
    page.open("/auth")  # Предполагаемый путь к странице логина
    return page