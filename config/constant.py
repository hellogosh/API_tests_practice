from dotenv import load_dotenv
import os
from dataclasses import dataclass
from typing import Dict
from enum import Enum

load_dotenv()

class HeaderType(Enum):
    """Типы HTTP заголовков"""
    JSON = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    FORM_URLENCODED = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json"
    }

@dataclass(frozen=True)
class AuthConfig:
    """Конфигурация для аутентификации"""
    username: str
    password: str
    scope: str = ""
    client_id: str = ""
    client_secret: str = ""


@dataclass(frozen=True)
class HeadersConfig:
    """Конфигурация HTTP заголовков"""
    auth: Dict[str, str]
    api: Dict[str, str]


class Config:
    BASE_URL = "https://api.fast-api.senior-pomidorov.ru/api/v1/"  # ← Фиксированный URL
    AUTH = AuthConfig(
        username=os.getenv("API_USERNAME"),
        password=os.getenv("API_PASSWORD")
    )
    HEADERS = HeadersConfig(
        auth={'Content-Type': 'application/x-www-form-urlencoded', 'Accept': 'application/json'},
        api={'Content-Type': 'application/json', 'Accept': 'application/json'}
    )

    @classmethod
    def validate(cls) -> None:
        required_vars = {
            "BASE_URL": cls.BASE_URL,
            "API_USERNAME": cls.AUTH.username,
            "API_PASSWORD": cls.AUTH.password
        }
        missing = [name for name, value in required_vars.items() if not value]
        if missing:
            raise ValueError(f"Проверьте .env файл - отсутствуют переменные: {', '.join(missing)}")


class Headers:
    AUTH = Config.HEADERS.auth
    API = Config.HEADERS.api


AUTH_DATA = {
    "username": Config.AUTH.username,
    "password": Config.AUTH.password,
    "scope": "",
    "client_id": "",
    "client_secret": ""
}

Config.validate()


__all__ = ['Config', 'Headers', 'AUTH_DATA']