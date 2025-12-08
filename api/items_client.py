from typing import Dict, Any, Union
from http_client.requester import HTTPClient
from models.item_models import ItemModel, ItemResponseModel
from requests import Response

class ItemsApiClient:
    def __init__(self, http_client: HTTPClient):
        self.http = http_client

    def create_item(self, item_data: Union[ItemModel, Dict[str, Any]]) -> Union[ItemResponseModel, Response]:
        if isinstance(item_data, ItemModel):
            json_data = item_data.model_dump()
        else:
            json_data = item_data

        response = self.http.post('/items/', json=json_data)

        if response.status_code in (200, 201):
            return ItemResponseModel(**response.json())
        return response

    def get_items(self, params: Dict[str,Any] = None) -> Union[list[ItemResponseModel], Response]:
        response = self.http.get('/items/', params=params)
        if response.status_code == 200:
            data = response.json()
            items = data.get('data', [])
            return [ItemResponseModel(**item) for item in items]
        else:
            return response

    def get_item(self, item_id: str) -> Union[ItemResponseModel, Response]:
        response = self.http.get(f'/items/{item_id}')
        if response.status_code == 200:
            return ItemResponseModel(**response.json())
        return response

    def update_item(self, item_id: str,
                    item_data: Union[ItemModel, Dict[str, Any]]) -> Union[ItemResponseModel, Response]:
        if isinstance(item_data, ItemModel):
            json_data = item_data.model_dump()
        else:
            json_data = item_data

        response = self.http.put(f'/items/{item_id}', json=json_data)

        if response.status_code == 200:
            return ItemResponseModel(**response.json())
        else:
            return response

    def delete_item(self, item_id: str) -> Union[bool, Response]:
        response = self.http.delete(f'/items/{item_id}')
        if response.status_code == 200:
            return True
        return response
