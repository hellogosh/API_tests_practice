from dotenv import load_dotenv
import os


# Загружаем переменные из .env файла
load_dotenv()

class Config:
    """Конфигурационные параметры"""
    BASE_URL = os.getenv("BASE_URL")
    API_USERNAME = os.getenv("API_USERNAME")
    API_PASSWORD = os.getenv("API_PASSWORD")

class Headers:
    """HTTP заголовки"""
    AUTH = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json'
    }
    API = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

AUTH_DATA = {
    "username": Config.API_USERNAME,
    "password": Config.API_PASSWORD,
    "scope": "",
    "client_id": "",
    "client_secret": ""
}

# Простая проверка при старте
assert Config.BASE_URL and Config.API_USERNAME and Config.API_PASSWORD, \
    "Проверьте .env файл - не все переменные загружены!"

print("Конфигурация загружена корректно")