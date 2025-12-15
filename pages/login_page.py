# pages/login_page.py
from selenium.webdriver.common.by import By
import allure
from .base_page import BasePage


class LoginPage(BasePage):
    """Page Object для страницы авторизации YouGile."""

    # ЛОКАТОРЫ (вынесены в константы)
    LOGIN_FIELD = (By.CSS_SELECTOR, "input[name='login']")
    PASSWORD_FIELD = (By.CSS_SELECTOR, "input[name='password']")
    SUBMIT_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    ERROR_MESSAGE = (By.CSS_SELECTOR, ".error-message")

    @allure.step("Выполнить авторизацию с логином {login} и паролем {password}")
    def login(self, login: str, password: str) -> None:
        """Основной метод авторизации."""
        self.find_element(self.LOGIN_FIELD).send_keys(login)
        self.find_element(self.PASSWORD_FIELD).send_keys(password)
        self.find_element(self.SUBMIT_BUTTON).click()

    @allure.step("Проверить наличие сообщения об ошибке")
    def is_error_message_displayed(self) -> bool:
        """Проверяет, отображается ли сообщение об ошибке."""
        try:
            return self.find_element(self.ERROR_MESSAGE, timeout=3).is_displayed()
        except TimeoutException:
            return False