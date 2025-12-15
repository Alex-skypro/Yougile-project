# tests/test_ui.py
import pytest
import allure
import time
from selenium.common.exceptions import TimeoutException
from pages.login_page import LoginPage
from pages.board_page import BoardPage
from config.settings import settings


@allure.epic("YouGile UI Tests")
@allure.feature("Авторизация")
class TestLoginUI:
    """UI-тесты для страницы авторизации YouGile."""

    @allure.title("Тест 1: Успешная авторизация с валидными данными")
    @allure.story("Позитивный сценарий")
    @allure.description("Проверка, что пользователь может войти с правильными логином и паролем")
    @pytest.mark.ui
    def test_successful_login(self, driver, login_page: LoginPage) -> None:
        """
        Соответствует пункту чек-листа:
        "Успешный вход с валидными данными перенаправляет на главную страницу"
        """
        with allure.step("Ввести валидный email и пароль"):
            login_page.login(
                login=settings.TEST_USER_LOGIN,
                password=settings.TEST_USER_PASSWORD
            )

        with allure.step("Проверить редирект на главную страницу"):
            # Ожидаем редирект на страницу с досками
            time.sleep(2)  # Небольшая задержка для редиректа
            assert "dashboard" in driver.current_url.lower() or "board" in driver.current_url.lower()
            
        with allure.step("Проверить отображение аватара пользователя"):
            login_page.take_screenshot("after_successful_login")
            # Здесь можно добавить проверку наличия элемента аватара
            assert driver.find_element("css selector", ".user-avatar") is not None

    @allure.title("Тест 2: Неуспешная авторизация с неверным паролем")
    @allure.story("Негативный сценарий")
    @allure.description("Проверка отображения ошибки при вводе неправильного пароля")
    @pytest.mark.ui
    def test_login_with_wrong_password(self, login_page: LoginPage) -> None:
        """
        Соответствует пункту чек-листа:
        "Попытка входа с неверным паролем отображает четкое сообщение об ошибке"
        """
        with allure.step("Ввести валидный email и неверный пароль"):
            login_page.login(
                login=settings.TEST_USER_LOGIN,
                password="wrong_password_123"
            )

        with allure.step("Проверить наличие сообщения об ошибке"):
            assert login_page.is_error_message_displayed() is True
            login_page.take_screenshot("wrong_password_error")

    @allure.title("Тест 3: Кнопка 'Войти' неактивна при пустых полях")
    @allure.story("Валидация формы")
    @allure.description("Проверка, что кнопка входа заблокирована пока не заполнены оба поля")
    @pytest.mark.ui
    def test_login_button_disabled_on_empty_fields(self, login_page: LoginPage) -> None:
        """
        Соответствует пункту чек-листа:
        "Кнопка 'Войти' активна только при заполненных полях логина и пароля"
        """
        with allure.step("Очистить поля ввода"):
            login_page.clear_login_fields()

        with allure.step("Проверить, что кнопка 'Войти' неактивна"):
            assert login_page.is_login_button_enabled() is False
            login_page.take_screenshot("disabled_login_button")

        with allure.step("Заполнить только поле логина"):
            login_page.enter_login(settings.TEST_USER_LOGIN)
            assert login_page.is_login_button_enabled() is False

        with allure.step("Заполнить оба поля"):
            login_page.enter_password("test")
            assert login_page.is_login_button_enabled() is True


@allure.epic("YouGile UI Tests")
@allure.feature("Управление досками")
class TestBoardsUI:
    """UI-тесты для работы с досками (проектами)."""

    @allure.title("Тест 4: Создание новой доски")
    @allure.story("Позитивный сценарий")
    @allure.description("Проверка создания доски с валидным названием")
    @pytest.mark.ui
    def test_create_new_board(self, authorized_driver) -> None:
        """
        Соответствует пункту чек-листа:
        "Создание доски с валидным названием (1-255 символов) проходит успешно"
        """
        board_page = BoardPage(authorized_driver)
        
        with allure.step("Открыть модальное окно создания доски"):
            board_page.open_create_board_modal()
            board_page.take_screenshot("create_board_modal_open")

        with allure.step("Ввести название доски и нажать 'Создать'"):
            board_title = f"Тестовая доска {int(time.time())}"
            board_page.create_board(board_title)

        with allure.step("Проверить, что доска появилась в списке"):
            assert board_page.is_board_present(board_title) is True
            board_page.take_screenshot("board_created_success")

    @allure.title("Тест 5: Попытка создания доски с пустым названием")
    @allure.story("Негативный сценарий")
    @allure.description("Проверка валидации поля названия доски")
    @pytest.mark.ui
    def test_create_board_with_empty_title(self, authorized_driver) -> None:
        """
        Соответствует пункту чек-листа:
        "Попытка создать доску с пустым названием блокируется, поле подсвечивается"
        """
        board_page = BoardPage(authorized_driver)
        
        with allure.step("Открыть модальное окно создания доски"):
            board_page.open_create_board_modal()

        with allure.step("Оставить поле названия пустым и попытаться создать"):
            board_page.create_board("")

        with allure.step("Проверить подсветку поля с ошибкой"):
            assert board_page.is_title_field_highlighted_error() is True
            board_page.take_screenshot("empty_title_validation_error")
            
        with allure.step("Проверить, что модальное окно не закрылось"):
            assert board_page.is_create_modal_still_open() is True