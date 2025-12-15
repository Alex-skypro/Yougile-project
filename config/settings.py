# config/settings.py
import os
from pathlib import Path
from dotenv import load_dotenv

# Загружаем переменные из .env файла
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)


class Settings:
    """Класс для хранения всех настроек приложения."""

    # UI Settings
    BASE_URL: str = os.getenv("BASE_URL", "https://yougile.com")
    BROWSER: str = os.getenv("BROWSER", "chrome")  # chrome/firefox
    HEADLESS: bool = os.getenv("HEADLESS", "False").lower() == 'true'
    IMPLICIT_WAIT: int = int(os.getenv("IMPLICIT_WAIT", "10"))

    # API Settings
    API_BASE_URL: str = os.getenv("API_BASE_URL", "https://yougile.com/api")

    # Test Data (БЕЗОПАСНО загружается из .env)
    TEST_USER_LOGIN: str = os.getenv("TEST_USER_LOGIN")
    TEST_USER_PASSWORD: str = os.getenv("TEST_USER_PASSWORD")
    TEST_COMPANY_ID: str = os.getenv("TEST_COMPANY_ID")

    # Пути
    PROJECT_ROOT = Path(__file__).parent.parent


# Создаём экземпляр настроек для импорта в других файлах
settings = Settings()

# Проверка при запуске, что критичные настройки загружены
if not settings.TEST_USER_LOGIN:
    raise ValueError("TEST_USER_LOGIN не найден в .env файле!")