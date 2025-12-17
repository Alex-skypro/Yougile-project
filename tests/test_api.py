"""API-тесты для YouGile."""
import pytest
import allure
import time
import requests
from typing import Dict, Any
from api.client import YouGileAPIClient
from config.settings import settings


@allure.epic("YouGile API Tests")
@allure.feature("Аутентификация через API")
class TestAuthAPI:
    """API-тесты для эндпоинтов авторизации."""

    @allure.title("Успешное получение токена авторизации")
    @allure.story("Позитивный сценарий")
    @pytest.mark.api
    @pytest.mark.smoke
    def test_successful_auth_get_token(self) -> None:
        """Проверка, что API возвращает токен при корректных данных."""
        client = YouGileAPIClient()
        
        with allure.step("Отправить запрос с валидными данными"):
            response_data = client.login(
                login=settings.TEST_USER_LOGIN,
                password=settings.TEST_USER_PASSWORD,
                company_id=settings.TEST_COMPANY_ID
            )

        with allure.step("Проверить структуру ответа"):
            assert "key" in response_data
            assert len(response_data["key"]) > 20
            assert "user" in response_data
            assert response_data["user"]["email"] == settings.TEST_USER_LOGIN

    @allure.title("Ошибка авторизации с неверным паролем")
    @allure.story("Негативный сценарий")
    @pytest.mark.api
    def test_auth_with_wrong_password_returns_error(self) -> None:
        """Проверка, что API возвращает ошибку при неверном пароле."""
        client = YouGileAPIClient()
        
        with allure.step("Отправить запрос с неверным паролем"):
            try:
                client.login(
                    login=settings.TEST_USER_LOGIN,
                    password="wrong_password_123",
                    company_id=settings.TEST_COMPANY_ID
                )
                pytest.fail("Ожидалась ошибка 401/400")
            except requests.exceptions.HTTPError as e:
                assert 400 <= e.response.status_code < 500

    @allure.title("Ошибка авторизации с пустым телом запроса")
    @allure.story("Негативный сценарий")
    @pytest.mark.api
    def test_auth_with_empty_body_returns_error(self) -> None:
        """Проверка валидации обязательных полей."""
        client = YouGileAPIClient()
        
        with allure.step("Отправить запрос с пустым JSON телом"):
            try:
                response = client._make_request("POST", "/auth/login", json={})
                response.raise_for_status()
                pytest.fail("Ожидалась ошибка 400")
            except requests.exceptions.HTTPError as e:
                assert e.response.status_code == 400


@allure.epic("YouGile API Tests")
@allure.feature("Управление досками через API")
class TestBoardsAPI:
    """API-тесты для работы с досками."""

    @allure.title("Создание новой доски с валидными данными")
    @allure.story("Позитивный сценарий")
    @pytest.mark.api
    def test_create_board_with_valid_data(self, api_client: YouGileAPIClient) -> None:
        """Проверка успешного создания доски через API."""
        board_title = f"API Test Board {int(time.time())}"
        
        with allure.step(f"Создать доску с названием '{board_title}'"):
            response_data = api_client.create_board(
                title=board_title,
                description="Доска создана тестами"
            )

        with allure.step("Проверить структуру ответа"):
            assert "id" in response_data
            assert response_data["title"] == board_title

    @allure.title("Попытка создания доски без авторизации")
    @allure.story("Негативный сценарий")
    @pytest.mark.api
    def test_create_board_without_auth_returns_401(self) -> None:
        """Проверка защиты эндпоинта авторизацией."""
        client = YouGileAPIClient()  # Клиент без токена
        
        with allure.step("Попытаться создать доску без токена"):
            try:
                client.create_board(title="Should Fail")
                pytest.fail("Ожидалась ошибка 401")
            except requests.exceptions.HTTPError as e:
                assert e.response.status_code == 401

    @allure.title("Получение списка досок после авторизации")
    @allure.story("Позитивный сценарий")
    @pytest.mark.api
    def test_get_boards_list_after_auth(self, api_client: YouGileAPIClient) -> None:
        """Проверка получения списка досок авторизованным пользователем."""
        with allure.step("Запросить список досок"):
            response = api_client._make_request("GET", "/boards")
            response.raise_for_status()
            boards_data = response.json()

        with allure.step("Проверить структуру ответа"):
            assert "content" in boards_data
            assert isinstance(boards_data["content"], list)