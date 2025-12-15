# tests/test_api.py
import pytest
import allure
import requests
from typing import Dict, Any
from api.client import YouGileAPIClient
from config.settings import settings


@allure.epic("YouGile API Tests")
@allure.feature("Аутентификация через API")
class TestAuthAPI:
    """API-тесты для эндпоинтов авторизации."""

    @allure.title("Тест 1: Успешное получение токена авторизации")
    @allure.story("Позитивный сценарий")
    @allure.description("Проверка, что API возвращает токен при корректных данных")
    @pytest.mark.api
    @pytest.mark.smoke
    def test_successful_auth_get_token(self) -> None:
        """
        Соответствует API-тест-кейсу: POS-01 (Успешная авторизация)
        """
        client = YouGileAPIClient()
        
        with allure.step("Отправить запрос на авторизацию с валидными данными"):
            response_data = client.login(
                login=settings.TEST_USER_LOGIN,
                password=settings.TEST_USER_PASSWORD,
                company_id=settings.TEST_COMPANY_ID
            )

        with allure.step("Проверить структуру и содержание ответа"):
            assert "key" in response_data
            assert len(response_data["key"]) > 20  # Токен должен быть достаточно длинным
            assert "user" in response_data
            assert "id" in response_data["user"]
            assert response_data["user"]["email"] == settings.TEST_USER_LOGIN

        with allure.step("Проверить, что токен сохранился в клиенте"):
            assert client.auth_token == response_data["key"]

    @allure.title("Тест 2: Ошибка авторизации с неверным паролем")
    @allure.story("Негативный сценарий")
    @allure.description("Проверка, что API возвращает ошибку при неверном пароле")
    @pytest.mark.api
    def test_auth_with_wrong_password_returns_error(self) -> None:
        """
        Соответствует API-тест-кейсу: NEG-01 (Авторизация с неверным паролем)
        """
        client = YouGileAPIClient()
        
        with allure.step("Отправить запрос с неверным паролем"):
            try:
                client.login(
                    login=settings.TEST_USER_LOGIN,
                    password="completely_wrong_password_12345",
                    company_id=settings.TEST_COMPANY_ID
                )
                # Если не выброшено исключение, тест должен упасть
                pytest.fail("Ожидалась ошибка 401/400, но авторизация прошла успешно!")
                
            except requests.exceptions.HTTPError as e:
                with allure.step("Проверить код и сообщение об ошибке"):
                    assert 400 <= e.response.status_code < 500
                    error_data = e.response.json()
                    assert "error" in error_data or "message" in error_data
                    allure.attach(
                        f"Status Code: {e.response.status_code}\nError: {error_data}",
                        name="Error Response"
                    )

    @allure.title("Тест 3: Ошибка авторизации с пустым телом запроса")
    @allure.story("Негативный сценарий")
    @allure.description("Проверка валидации обязательных полей")
    @pytest.mark.api
    def test_auth_with_empty_body_returns_error(self) -> None:
        """
        Соответствует API-тест-кейсу: NEG-02 (Авторизация с пустым телом запроса)
        """
        client = YouGileAPIClient()
        
        with allure.step("Отправить запрос с пустым JSON телом"):
            try:
                # Используем низкоуровневый метод для отправки пустого тела
                response = client._make_request("POST", "/auth/login", json={})
                response.raise_for_status()
                pytest.fail("Ожидалась ошибка 400, но запрос прошёл успешно!")
                
            except requests.exceptions.HTTPError as e:
                with allure.step("Проверить код ошибки 400"):
                    assert e.response.status_code == 400
                    allure.attach(
                        f"Status: {e.response.status_code}\nBody: {e.response.text}",
                        name="Validation Error"
                    )


@allure.epic("YouGile API Tests")
@allure.feature("Управление досками через API")
class TestBoardsAPI:
    """API-тесты для работы с досками."""

    @allure.title("Тест 4: Создание новой доски с валидными данными")
    @allure.story("Позитивный сценарий")
    @allure.description("Проверка успешного создания доски через API")
    @pytest.mark.api
    def test_create_board_with_valid_data(self, api_client: YouGileAPIClient) -> None:
        """
        Соответствует API-тест-кейсу: POS-03 (Создание новой доски)
        """
        board_title = f"API Test Board {int(time.time())}"
        board_description = "Доска создана автоматизированными тестами"
        
        with allure.step(f"Создать доску с названием '{board_title}'"):
            response_data = api_client.create_board(
                title=board_title,
                description=board_description
            )

        with allure.step("Проверить структуру ответа"):
            assert "id" in response_data
            assert response_data["title"] == board_title
            assert response_data["description"] == board_description
            assert "createdAt" in response_data
            assert "updatedAt" in response_data
            
        with allure.step("Сохранить ID доски для последующих тестов"):
            # Можно сохранить в переменную класса или фикстуру для очистки
            pytest.board_id = response_data["id"]
            allure.attach(f"Board ID: {response_data['id']}", name="Created Board")

    @allure.title("Тест 5: Попытка создания доски без авторизации")
    @allure.story("Негативный сценарий")
    @allure.description("Проверка защиты эндпоинта авторизацией")
    @pytest.mark.api
    def test_create_board_without_auth_returns_401(self) -> None:
        """
        Соответствует API-тест-кейсу: NEG-03 (Создание доски без авторизации)
        """
        client = YouGileAPIClient()  # Клиент без токена
        
        with allure.step("Попытаться создать доску без токена авторизации"):
            try:
                client.create_board(title="Should Fail Without Auth")
                pytest.fail("Ожидалась ошибка 401 Unauthorized!")
                
            except requests.exceptions.HTTPError as e:
                with allure.step("Проверить код ошибки 401"):
                    assert e.response.status_code == 401
                    error_data = e.response.json()
                    assert "error" in error_data
                    assert "unauthorized" in error_data["error"].lower() or "auth" in error_data["error"].lower()
                    
                    allure.attach(
                        f"Status: 401\nError: {error_data['error']}",
                        name="Authentication Error"
                    )