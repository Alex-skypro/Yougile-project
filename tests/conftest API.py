# tests/conftest.py (продолжение)
@pytest.fixture(scope="session")
def api_client():
    """Фикстура возвращает авторизованный API-клиент."""
    from api.client import YouGileAPIClient
    from config.settings import settings

    client = YouGileAPIClient()
    # Авторизуемся один раз на всю сессию тестов
    client.login(
        login=settings.TEST_USER_LOGIN,
        password=settings.TEST_USER_PASSWORD,
        company_id=settings.TEST_COMPANY_ID
    )
    return client