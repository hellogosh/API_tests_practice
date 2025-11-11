
import requests
from typing import Dict, Any, Union


class BasicAPIClient:  # базовые методы запросов к API
    def __init__(self, session: requests.Session, base_url: str):
        self.session = session
        self.base_url = base_url.rstrip('/')

    def create_item(self, item_data: Union['Item', Dict[str, Any]]) -> requests.Response:
        # Работаем как с объектом Item, так и со словарем
        if hasattr(item_data, 'model_dump'):
            json_data = item_data.model_dump()
        else:
            json_data = item_data
        return self.session.post(f'{self.base_url}/items/', json=json_data)

    def get_items(self, params: Dict[str, Any] = None) -> requests.Response:
        return self.session.get(f'{self.base_url}/items/', params=params)

    def update_item(self, item_id: str, item_data: Union['Item', Dict[str, Any]], headers=None) -> requests.Response:
        url = f'{self.base_url}/items/{item_id}'
        # Работаем как с объектом Item, так и со словарем
        if hasattr(item_data, 'model_dump'):
            json_data = item_data.model_dump()
        else:
            json_data = item_data
        return self.session.put(url, json=json_data, headers=headers)

    def delete_item(self, item_id: str) -> requests.Response:
        url = f'{self.base_url}/items/{item_id}'
        return self.session.delete(url)

    def create_item_no_auth(self, item_data: dict) -> requests.Response:
        # Используем requests напрямую без сессии с авторизацией
        return requests.post(f'{self.base_url}/items/', json=item_data)