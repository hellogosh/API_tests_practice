import requests
import pytest
from config.constant import BASE_URL, AUTH_HEADERS, API_HEADERS, AUTH_DATA
from faker import Faker

fake = Faker()

@pytest.fixture(scope="session") #фикстура для получения токена и сохранения авторизованной сессии.
def auth_session():
    session = requests.Session()
    response = session.post(f'{BASE_URL}login/access-token',
                                headers=AUTH_HEADERS,
                                data=AUTH_DATA)
    assert response.status_code == 200, f"ошибка авторизации {response.status_code}, {response.text}"
    token = response.json().get("access_token")
    assert token, "Токен не найден"

    session.headers.update(API_HEADERS)
    session.headers.update({"Authorization": f"Bearer {token}"})
    return session

@pytest.fixture() #фикстура генерирующая данные для создания нового элемента
def item_data():
    return {
        "title": fake.word().capitalize(),
        "description": fake.sentence(nb_words=10)
    }