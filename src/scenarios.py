from src.basic_api_methods import ItemsApiManager
from src.models.data_models import ItemModel
from src.constant import HeaderType


class ItemScenarios: #методы, которые комбинируют базовые вызовы API для часто встречающихся сценариев
    def __init__(self, api_client: ItemsApiManager):
        self.api = api_client

    def create_and_delete_item(self, item: ItemModel):
        create_resp = self.api.create_item(item)
        item_id = create_resp.json().get('id')
        del_resp = None
        if item_id:
            del_resp = self.api.delete_item(item_id)
        return create_resp, del_resp

    def create_and_update_item(self, item: ItemModel, upd_suffix='_updated'):
        create_resp = self.api.create_item(item)
        item_id = create_resp.json().get('id')
        upd_resp = None
        if item_id:
            upd_item = ItemModel(
                title=item.title + upd_suffix,
                description=item.description + ' updated'
            )
            upd_resp = self.api.update_item(item_id, upd_item, HeaderType.JSON.value)
            return create_resp, upd_resp
