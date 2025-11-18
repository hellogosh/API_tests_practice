import requests
import pytest
from src.constant import Config, Headers, AUTH_DATA
from faker import Faker
from src.basic_api_methods import BasicAPIClient
from src.scenarios import ItemScenarios
from models.data_models import Item, ItemUpdate

fake = Faker()

BASE_URL = Config.BASE_URL
AUTH_HEADERS = Headers.AUTH
API_HEADERS = Headers.API

print("=== CONFTEST DEBUG INFO ===")
print(f"BASE_URL: {BASE_URL}")
print(f"AUTH_HEADERS: {AUTH_HEADERS}")
print(f"AUTH_DATA username: {AUTH_DATA['username']}")
print(f"AUTH_DATA password: {AUTH_DATA['password']}")
print("===========================")

@pytest.fixture(scope="session")
def auth_session():
    session = requests.Session()


    print(f"Auth URL: {BASE_URL}login/access-token")
    print(f"Auth headers: {AUTH_HEADERS}")
    print(f"Auth data: {AUTH_DATA}")


    response = session.post(f'{BASE_URL}login/access-token',
                            headers=AUTH_HEADERS,  # ← ИСПОЛЬЗУЕМ AUTH_HEADERS, а не Headers
                            data=AUTH_DATA)

    print(f"Response status: {response.status_code}")
    print(f"Response text: {response.text}")

    assert response.status_code == 200, f"ошибка авторизации {response.status_code}, {response.text}"

    token_data = response.json()
    session.headers.update({'Authorization': f"Bearer {token_data['access_token']}"})
    return session

@pytest.fixture()
def item_data():
    return {
        "title": fake.word().capitalize(),
        "description": fake.sentence(nb_words=10)
    }

@pytest.fixture()
def valid_payload():
    """Генерирует валидные данные через модель"""
    return Item.generate_valid()
@pytest.fixture
def invalid_payload():
    """Генерирует невалидные данные через модель"""
    return Item.generate_invalid()

@pytest.fixture
def update_payload():
    """Данные для полного обновления (PUT)"""
    return ItemUpdate.generate_full_update()

@pytest.fixture
def partial_update_payload():
    """Данные для частичного обновления (PATCH)"""
    return ItemUpdate.generate_partial_update()

@pytest.fixture
def scenarios(auth_session):
    api_client = BasicAPIClient(auth_session, BASE_URL)
    return ItemScenarios(api_client)


@pytest.fixture
def created_item(auth_session, valid_payload):
    """Создает item и возвращает его данные"""
    response = auth_session.post(f"{BASE_URL}items", json=valid_payload)
    assert response.status_code == 201, f"Не удалось создать item: {response.text}"
    item_data = response.json()
    yield item_data

    # Очистка после теста
    item_id = item_data["id"]
    auth_session.delete(f"{BASE_URL}items/{item_id}")


@pytest.fixture
def scenarios(auth_session):
    api_client = BasicAPIClient(auth_session, BASE_URL)
    return ItemScenarios(api_client)