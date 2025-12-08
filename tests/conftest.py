import sys
import os

# Добавляем корень проекта в Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from config.constant import Config, AUTH_DATA, Headers
from scenarios.items_scenarios import ItemScenarios
from models.item_models import ItemModel, ItemResponseModel
from http_client.requester import HTTPClient
from api.items_client import ItemsApiClient

@pytest.fixture(scope="session")
def http_client():
    """Базовый HTTP клиент без авторизации"""
    return HTTPClient(base_url=Config.BASE_URL)


@pytest.fixture(scope="session")
def auth_http_client(http_client):
    """Авторизованный HTTP клиент"""
    # Авторизуемся
    response = http_client.post(
        'login/access-token',
        data=AUTH_DATA,
        headers={'Content-Type': 'application/x-www-form-urlencoded'}
    )
    print(f"DEBUG Auth response: {response.status_code} {response.text}")

    assert response.status_code == 200, f"Ошибка авторизации:{response.status_code} - {response.text}"

    token_data = response.json()
    access_token = token_data.get('access_token')

    if not access_token:
        pytest.fail("Токен не получен в ответе авторизации")

    http_client.set_headers({
        'Authorization': f"Bearer {token_data['access_token']}",
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    })

    return http_client


@pytest.fixture
def scenarios(auth_http_client):
    """Готовые тестовые сценарии"""
    api_client = ItemsApiClient(auth_http_client)
    return ItemScenarios(api_client)


@pytest.fixture
def created_item(scenarios):
    """Создает временный item для тестов"""
    item_data = ItemModel.generate_valid()
    response = scenarios.api.create_item(item_data)

    # Проверяем тип результата
    if isinstance(response, ItemResponseModel):
        # Успешное создание
        assert response.id is not None, f"Не удалось создать item"
        yield response
        # Удаляем после теста
        scenarios.api.delete_item(response.id)
    else:
        # Ошибка создания
        pytest.fail(f"Не удалось создать item: {response.status_code} - {response.text}")


@pytest.fixture
def unauthorized_http_client():
    """HTTP клиент без авторизации"""
    return HTTPClient(base_url=Config.BASE_URL)

@pytest.fixture
def unauthorized_api(unauthorized_http_client):
    """API клиент без авторизации (новый)"""
    return ItemsApiClient(unauthorized_http_client)