"""UI-тесты для YouGile."""
import pytest
import allure
import time
from pages.login_page import LoginPage
from pages.board_page import BoardPage
from config.settings import settings


@allure.epic("YouGile UI Tests")
@allure.feature("Авторизация")
class TestLoginUI:
    """UI-тесты для страницы авторизации YouGile."""

    @allure.title("Успешная авторизация с валидными данными")
    @allure.story("Позитивный сценарий")
    @pytest.mark.ui
    def test_successful_login(self, driver, login_page: LoginPage) -> None:
        """Проверка входа с правильными логином и паролем."""
        with allure.step("Ввести валидные учётные данные"):
            login_page.login(
                login=settings.TEST_USER_LOGIN,
                password=settings.TEST_USER_PASSWORD
            )

        with allure.step("Проверить редирект на главную страницу"):
            time.sleep(2)
            assert any(keyword in driver.current_url.lower() 
                      for keyword in ["dashboard", "board", "project"])
            login_page.take_screenshot("after_successful_login")

    @allure.title("Неуспешная авторизация с неверным паролем")
    @allure.story("Негативный сценарий")
    @pytest.mark.ui
    def test_login_with_wrong_password(self, login_page: LoginPage) -> None:
        """Проверка отображения ошибки при неверном пароле."""
        with allure.step("Ввести валидный email и неверный пароль"):
            login_page.login(
                login=settings.TEST_USER_LOGIN,
                password="wrong_password_123"
            )

        with allure.step("Проверить наличие сообщения об ошибке"):
            assert login_page.is_error_message_displayed()
            login_page.take_screenshot("wrong_password_error")

    @allure.title("Кнопка 'Войти' неактивна при пустых полях")
    @allure.story("Валидация формы")
    @pytest.mark.ui
    def test_login_button_disabled_on_empty_fields(self, login_page: LoginPage) -> None:
        """Проверка, что кнопка входа заблокирована при пустых полях."""
        with allure.step("Очистить поля ввода"):
            login_page.clear_login_fields()

        with allure.step("Проверить, что кнопка 'Войти' неактивна"):
            assert not login_page.is_login_button_enabled()
            login_page.take_screenshot("disabled_login_button")

    @allure.title("Поле пароля скрывает вводимые символы")
    @allure.story("Безопасность")
    @pytest.mark.ui
    def test_password_field_masked(self, login_page: LoginPage) -> None:
        """Проверка, что пароль скрыт звёздочками."""
        password_field = login_page.find_element(login_page.PASSWORD_FIELD)
        
        with allure.step("Проверить тип поля пароля"):
            assert password_field.get_attribute("type") == "password"
            login_page.take_screenshot("password_field_masked")


@allure.epic("YouGile UI Tests")
@allure.feature("Управление досками")
class TestBoardsUI:
    """UI-тесты для работы с досками."""

    @allure.title("Создание новой доски с валидным названием")
    @allure.story("Позитивный сценарий")
    @pytest.mark.ui
    def test_create_new_board(self, authorized_driver) -> None:
        """Проверка создания доски с валидным названием."""
        board_page = BoardPage(authorized_driver)
        
        with allure.step("Открыть модальное окно создания доски"):
            board_page.open_create_board_modal()
            board_page.take_screenshot("create_board_modal")

        with allure.step("Ввести название доски и нажать 'Создать'"):
            board_title = f"Тестовая доска {int(time.time())}"
            board_page.create_board(board_title)

        with allure.step("Проверить, что доска появилась в списке"):
            assert board_page.is_board_present(board_title)
            board_page.take_screenshot("board_created")

    @allure.title("Попытка создания доски с пустым названием")
    @allure.story("Негативный сценарий")
    @pytest.mark.ui
    def test_create_board_with_empty_title(self, authorized_driver) -> None:
        """Проверка валидации поля названия доски."""
        board_page = BoardPage(authorized_driver)
        
        with allure.step("Открыть модальное окно создания доски"):
            board_page.open_create_board_modal()

        with allure.step("Оставить поле названия пустым"):
            board_page.create_board("")

        with allure.step("Проверить подсветку поля с ошибкой"):
            assert board_page.is_title_field_highlighted_error()
            board_page.take_screenshot("empty_title_error")