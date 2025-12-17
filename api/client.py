"""Клиент для работы с YouGile API."""
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
        
        if self.auth_token:
            headers["Authorization"] = f"Bearer {self.auth_token}"
        if "json" in kwargs:
            headers["Content-Type"] = "application/json"
            
        with allure.step(f"{method.upper()} {url}"):
            response = self.session.request(
                method, url, 
                headers=headers, 
                **kwargs
            )
            
            allure.attach(
                f"Request: {method} {url}\n"
                f"Headers: {headers}\n"
                f"Body: {kwargs.get('json', {})}",
                name="Request Details"
            )
            allure.attach(
                f"Status: {response.status_code}\n"
                f"Response: {response.text[:500]}",
                name="Response Details"
            )
            
            return response

    @allure.step("Авторизация в API YouGile")
    def login(self, login: str, password: str, company_id: str) -> Dict[str, Any]:
        """Выполняет авторизацию и сохраняет токен."""
        payload = {
            "login": login,
            "password": password,
            "companyId": company_id
        }
        response = self._make_request("POST", "/auth/login", json=payload)
        response.raise_for_status()
        data = response.json()
        self.auth_token = data.get("key")
        return data

    @allure.step("Создание новой доски")
    def create_board(self, title: str, description: str = "") -> Dict[str, Any]:
        """Создаёт новую доску (проект)."""
        payload = {"title": title, "description": description}
        response = self._make_request("POST", "/boards", json=payload)
        response.raise_for_status()
        return response.json()

    @allure.step("Получение информации о доске")
    def get_board(self, board_id: str) -> Dict[str, Any]:
        """Получает информацию о конкретной доске."""
        response = self._make_request("GET", f"/boards/{board_id}")
        response.raise_for_status()
        return response.json()