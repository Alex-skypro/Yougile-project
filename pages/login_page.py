"""Page Object для страницы авторизации YouGile."""
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import allure
from .base_page import BasePage


class LoginPage(BasePage):
    """Page Object для страницы авторизации YouGile."""

    # ЛОКАТОРЫ
    LOGIN_FIELD = (By.CSS_SELECTOR, "input[name='login'], input[type='email']")
    PASSWORD_FIELD = (By.CSS_SELECTOR, "input[name='password'], input[type='password']")
    SUBMIT_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    ERROR_MESSAGE = (By.CSS_SELECTOR, ".error-message, .alert-danger, [data-qa='error-message']")

    @allure.step("Выполнить авторизацию с логином {login}")
    def login(self, login: str, password: str) -> None:
        """Основной метод авторизации."""
        self.find_element(self.LOGIN_FIELD).send_keys(login)
        self.find_element(self.PASSWORD_FIELD).send_keys(password)
        self.find_element(self.SUBMIT_BUTTON).click()

    @allure.step("Очистить поля логина и пароля")
    def clear_login_fields(self) -> None:
        """Очищает поля ввода логина и пароля."""
        self.find_element(self.LOGIN_FIELD).clear()
        self.find_element(self.PASSWORD_FIELD).clear()

    @allure.step("Ввести логин {login}")
    def enter_login(self, login: str) -> None:
        """Вводит логин в соответствующее поле."""
        self.find_element(self.LOGIN_FIELD).send_keys(login)

    @allure.step("Ввести пароль")
    def enter_password(self, password: str) -> None:
        """Вводит пароль в соответствующее поле."""
        self.find_element(self.PASSWORD_FIELD).send_keys(password)

    @allure.step("Проверить наличие сообщения об ошибке")
    def is_error_message_displayed(self) -> bool:
        """Проверяет, отображается ли сообщение об ошибке."""
        try:
            return self.find_element(self.ERROR_MESSAGE, timeout=3).is_displayed()
        except TimeoutException:
            return False

    @allure.step("Проверить активность кнопки 'Войти'")
    def is_login_button_enabled(self) -> bool:
        """Проверяет, активна ли кнопка отправки формы."""
        return self.find_element(self.SUBMIT_BUTTON).is_enabled()