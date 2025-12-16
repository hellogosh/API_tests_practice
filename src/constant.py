from dotenv import load_dotenv
import os
from dataclasses import dataclass
from typing import Dict, ClassVar
from enum import Enum

load_dotenv()


class HeaderType(Enum):
    """Enum с типами HTTP заголовков"""
    JSON = "json"
    FORM_URLENCODED = "form_urlencoded"

    def get_headers(self) -> Dict[str, str]:
        """Возвращает соответствующие заголовки для типа"""
        headers_map = {
            HeaderType.JSON: {
                "Content-Type": "application/json",
                "Accept": "application/json"
            },
            HeaderType.FORM_URLENCODED: {
                "Content-Type": "application/x-www-form-urlencoded",
                "Accept": "application/json"
            }
        }
        return headers_map[self]


@dataclass(frozen=True)
class AuthConfig:
    """Конфигурация для аутентификации"""
    username: str
    password: str
    scope: str = ""
    client_id: str = ""
    client_secret: str = ""

    @property
    def form_data(self) -> Dict[str, str]:
        """Возвращает данные для формы авторизации"""
        data = {
            "username": self.username,
            "password": self.password,
        }
        if self.scope:
            data["scope"] = self.scope
        if self.client_id:
            data["client_id"] = self.client_id
        if self.client_secret:
            data["client_secret"] = self.client_secret
        return data


class APIConfig:
    """Основной класс конфигурации API"""

    # Базовые константы
    BASE_URL: ClassVar[str] = "https://api.fast-api.senior-pomidorov.ru/api/v1/"

    # Конфигурация аутентификации (инициализируется при загрузке модуля)
    _auth_config: ClassVar[AuthConfig] = None

    @classmethod
    def _initialize(cls) -> None:
        """Инициализация конфигурации"""
        if cls._auth_config is None:
            cls._auth_config = AuthConfig(
                username=os.getenv("API_USERNAME", ""),
                password=os.getenv("API_PASSWORD", "")
            )

    @classmethod
    def get_auth_config(cls) -> AuthConfig:
        """Получить конфигурацию аутентификации"""
        cls._initialize()
        return cls._auth_config

    @classmethod
    def get_auth_data(cls) -> Dict[str, str]:
        """Получить данные для авторизации"""
        return cls.get_auth_config().form_data


    @classmethod
    def get_auth_headers(cls) -> Dict[str, str]:
        """Получить заголовки для аутентификации"""
        return HeaderType.FORM_URLENCODED.get_headers()

    @classmethod
    def get_api_headers(cls) -> Dict[str, str]:
        """Получить заголовки для API запросов"""
        return HeaderType.JSON.get_headers()

    @classmethod
    def validate(cls) -> None:
        """Валидация конфигурации"""
        auth_config = cls.get_auth_config()
        missing = []

        # Проверка переменных окружения
        if not auth_config.username:
            missing.append("API_USERNAME")
        if not auth_config.password:
            missing.append("API_PASSWORD")

        # Проверка BASE_URL
        if not cls.BASE_URL or not cls.BASE_URL.startswith(("http://", "https://")):
            raise ValueError("BASE_URL должен быть валидным URL")

        if missing:
            raise ValueError(
                f"Проверьте .env файл - отсутствуют переменные: {', '.join(missing)}"
            )


# Инициализация и валидация при загрузке модуля
APIConfig.validate()