import requests
from typing import Dict, Any, Union


class ItemsApiManager:  # базовые методы запросов к API
    def __init__(self, session: requests.Session, base_url: str):
        self.session = session
        self.items_url = f"{base_url.rstrip('/')}/items/"

    def create_item(self, item_data: Union['ItemModel', Dict[str, Any]]) -> requests.Response:
        # Работаем как с объектом Item, так и со словарем
        if hasattr(item_data, 'model_dump'):
            json_data = item_data.model_dump()
        else:
            json_data = item_data
        return self.session.post(self.items_url, json=json_data)

    def create_item_no_auth(self, item_data: dict) -> requests.Response:
        # Используем requests напрямую без сессии с авторизацией
        return requests.post(self.items_url, json=item_data)

    def get_items(self, params: Dict[str, Any] = None) -> requests.Response:
        return self.session.get(self.items_url, params=params)

    def update_item(self, item_id: str, item_data: Union['ItemModel', Dict[str, Any]], headers=None) -> requests.Response:
        url = f'{self.items_url.rstrip("/")}/{item_id}'
        # Работаем как с объектом Item, так и со словарем
        if hasattr(item_data, 'model_dump'):
            json_data = item_data.model_dump()
        else:
            json_data = item_data
        return self.session.put(url, json=json_data, headers=headers)

    def delete_item(self, item_id: str) -> requests.Response:
        url = f'{self.items_url.rstrip("/")}/{item_id}'
        return self.session.delete(url)
