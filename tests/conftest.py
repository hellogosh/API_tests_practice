import requests
import pytest
from config.constant import BASE_URL, AUTH_HEADERS, API_HEADERS, AUTH_DATA
from faker import Faker
from tests.test_api import BasicAPIClient, ItemScenarios
fake = Faker()


print("=== CONFTEST DEBUG INFO ===")
print(f"BASE_URL: {BASE_URL}")
print(f"AUTH_DATA username: {AUTH_DATA['username']}")
print(f"AUTH_DATA password: {AUTH_DATA['password']}")
print("===========================")

# @pytest.fixture(scope="session") #фикстура для получения токена и сохранения авторизованной сессии.
# def auth_session():
#     session = requests.Session()
#     response = session.post(f'{BASE_URL}login/access-token',
#                                 headers=AUTH_HEADERS,
#                                 data=AUTH_DATA)
#     assert response.status_code == 200, f"ошибка авторизации {response.status_code}, {response.text}"
#     token = response.json().get("access_token")
#     assert token, "Токен не найден"
#
#     session.headers.update(API_HEADERS)
#     session.headers.update({"Authorization": f"Bearer {token}"})
#     return session

@pytest.fixture(scope="session")
def auth_session():
    session = requests.Session()

    # Добавьте отладочную информацию
    print(f"Auth URL: {BASE_URL}login/access-token")
    print(f"Auth headers: {AUTH_HEADERS}")
    print(f"Auth data: {AUTH_DATA}")

    response = session.post(f'{BASE_URL}login/access-token',
                            headers=AUTH_HEADERS,
                            data=AUTH_DATA)

    print(f"Response status: {response.status_code}")
    print(f"Response text: {response.text}")

    assert response.status_code == 200, f"ошибка авторизации {response.status_code}, {response.text}"

    token_data = response.json()
    session.headers.update({'Authorization': f"Bearer {token_data['access_token']}"})
    return session
@pytest.fixture() #фикстура генерирующая данные для создания нового элемента
def item_data():
    return {
        "title": fake.word().capitalize(),
        "description": fake.sentence(nb_words=10)
    }

@pytest.fixture
def invalid_payload():
    return [
        {"title": "", "description": "valid description"},
        {"title": "a" * 300, "description": "desc"},
        {"title": "valid", "description": "a" * 2000},
        {"title": None, "description": "desc"},
        {"description": "desc only"},
    ]

@pytest.fixture
def scenarios(auth_session):
    api_client = BasicAPIClient(auth_session, BASE_URL)
    return ItemScenarios(api_client)