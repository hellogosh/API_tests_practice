import requests
import pytest
from src.constant import Config, AUTH_DATA
from src.basic_api_methods import ItemsApiManager
from src.scenarios import ItemScenarios
from src.models.data_models import ItemModel

print("=== CONFTEST DEBUG INFO ===")
print(f"BASE_URL: {Config.BASE_URL}")
print(f"AUTH_DATA username: {AUTH_DATA['username']}")
print("===========================")


@pytest.fixture(scope="session")
def auth_session():
    """Создает авторизованную сессию"""
    session = requests.Session()

    response = session.post(
        f'{Config.BASE_URL}login/access-token',
        headers=Config.HEADERS.auth,
        data=AUTH_DATA
    )

    assert response.status_code == 200, f"Ошибка авторизации: {response.text}"

    token_data = response.json()
    session.headers.update({'Authorization': f"Bearer {token_data['access_token']}"})
    return session


@pytest.fixture
def scenarios(auth_session):
    """Готовые тестовые сценарии"""
    api_client = ItemsApiManager(auth_session, Config.BASE_URL)
    return ItemScenarios(api_client)


@pytest.fixture
def created_item(scenarios):
    """Создает временный item для тестов (автоочистка)"""

    # Используем модель для генерации данных
    item_data = ItemModel.generate_valid()
    response = scenarios.api.create_item(item_data)

    assert response.status_code == 200, f"Не удалось создать item: {response.text}"
    item_data = response.json()

    yield item_data

    # Автоматическая очистка
    item_id = item_data["id"]
    scenarios.api.delete_item(item_id)