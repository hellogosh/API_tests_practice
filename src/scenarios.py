from src.basic_api_methods import BasicAPIClient
from models.data_models import Item


class ItemScenarios: #методы, которые комбинируют базовые вызовы API для часто встречающихся сценариев
    def __init__(self, api_client: BasicAPIClient):
        self.api = api_client

    def create_and_delete_item(self, item: Item):
        create_resp = self.api.create_item(item)
        item_id = create_resp.json().get('id')
        del_resp = None
        if item_id:
            del_resp = self.api.delete_item(item_id)
        return create_resp, del_resp

    def create_and_update_item(self, item: Item, upd_suffix='_updated'):
        create_resp = self.api.create_item(item)
        item_id = create_resp.json().get('id')
        upd_resp = None
        if item_id:
            upd_item = Item(
                title=item.title + upd_suffix,
                description=item.description + ' updated'
            )
            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
            upd_resp = self.api.update_item(item_id, upd_item, headers)
        return create_resp, upd_resp
