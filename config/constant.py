from dotenv import load_dotenv
import os

# Загружаем переменные из .env файла
load_dotenv()

# Используем новые имена переменных (чтобы избежать конфликта с системной переменной USERNAME в Windows)
BASE_URL = os.getenv("BASE_URL")
API_USERNAME = os.getenv("API_USERNAME")  # ← Новое имя!
API_PASSWORD = os.getenv("API_PASSWORD")  # ← Новое имя!

print(f"=== LOADED FROM .env ===")
print(f"BASE_URL: {BASE_URL}")
print(f"API_USERNAME: {API_USERNAME}")
print(f"API_PASSWORD: {'*' * len(API_PASSWORD) if API_PASSWORD else 'NOT SET'}")
print(f"========================")

# Проверяем, что все переменные загружены
if not all([BASE_URL, API_USERNAME, API_PASSWORD]):
    missing = []
    if not BASE_URL: missing.append("BASE_URL")
    if not API_USERNAME: missing.append("API_USERNAME")
    if not API_PASSWORD: missing.append("API_PASSWORD")
    raise ValueError(f"Не загружены переменные окружения: {', '.join(missing)}. Проверьте файл .env")

# Убедимся, что BASE_URL заканчивается на /
if not BASE_URL.endswith('/'):
    BASE_URL += '/'

AUTH_HEADERS = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': 'application/json'
}

API_HEADERS = {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

AUTH_DATA = {
    "username": API_USERNAME,  # ← Используем новую переменную здесь!
    "password": API_PASSWORD,  # ← И здесь!
    "scope": "",
    "client_id": "",
    "client_secret": ""
}