"""Конфигурация фикстур для тестов."""
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from api.client import YouGileAPIClient
from config.settings import settings


@pytest.fixture(scope="function")
def driver():
    """Фикстура для создания и закрытия браузера."""
    options = webdriver.ChromeOptions()
    if settings.HEADLESS:
        options.add_argument("--headless")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    driver.implicitly_wait(settings.IMPLICIT_WAIT)
    
    yield driver
    
    driver.quit()


@pytest.fixture(scope="session")
def api_client():
    """Фикстура возвращает авторизованный API-клиент."""
    client = YouGileAPIClient()
    client.login(
        login=settings.TEST_USER_LOGIN,
        password=settings.TEST_USER_PASSWORD,
        company_id=settings.TEST_COMPANY_ID
    )
    return client


@pytest.fixture(scope="function")
def authorized_driver(driver, api_client):
    """
    Фикстура возвращает драйвер с уже выполненной авторизацией
    через куки (оптимизация для UI-тестов).
    """
    driver.get(settings.BASE_URL)
    driver.add_cookie({
        "name": "auth_token",
        "value": api_client.auth_token,
        "domain": ".yougile.com"
    })
    driver.refresh()
    
    return driver


@pytest.fixture
def login_page(driver):
    """Фикстура возвращает экземпляр LoginPage."""
    from pages.login_page import LoginPage
    page = LoginPage(driver)
    page.open("/auth")
    return page