# api/client.py
import requests
import allure
from typing import Optional, Dict, Any
from config.settings import settings


class YouGileAPIClient:
    """Клиент для работы с YouGile API."""

    def __init__(self):
        self.base_url = settings.API_BASE_URL
        self.session = requests.Session()
        self.auth_token: Optional[str] = None

    def _make_request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        """Базовый метод для выполнения HTTP-запросов."""
        url = f"{self.base_url}{endpoint}"
        headers = kwargs.get("headers", {})

        # Если есть токен, добавляем его в заголовки
        if self.auth_token:
            headers["Authorization"] = f"Bearer {self.auth_token}"

        with allure.step(f"{method.upper()} {url}"):
            response = self.session.request(method, url, headers=headers, **kwargs)
            # Логирование для отладки (можно вынести в Allure)
            allure.attach(f"Request Headers: {headers}", name="Request")
            allure.attach(f"Response Status: {response.status_code}\nResponse Body: {response.text}", name="Response")
            return response

    @allure.step("Авторизоваться в API")
    def login(self, login: str, password: str, company_id: str) -> Dict[str, Any]:
        """Выполняет авторизацию и сохраняет токен."""
        payload = {
            "login": login,
            "password": password,
            "companyId": company_id
        }
        response = self._make_request("POST", "/auth/login", json=payload)
        response.raise_for_status()  # Выбросит исключение при статусе 4xx/5xx
        data = response.json()
        self.auth_token = data.get("key")  # Сохраняем токен
        return data

    @allure.step("Создать новую доску")
    def create_board(self, title: str, description: str = "") -> Dict[str, Any]:
        """Создаёт новую доску (проект)."""
        payload = {"title": title, "description": description}
        response = self._make_request("POST", "/boards", json=payload)
        response.raise_for_status()
        return response.json()