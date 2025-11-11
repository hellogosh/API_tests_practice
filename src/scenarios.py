from src.basic_api_methods import BasicAPIClient
from src.data_models import Item


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
    #
    # def create_item_invalid(self, invalid_data):
    #     return self.api.create_item(invalid_data)
    #
    # def update_non_existent_item(self, fake_id, data):
    #     return self.api.update_item(fake_id, data)
    #
    # def delete_non_existent_item(self, fake_id):
    #     return self.api.delete_item(fake_id)
    #
    # def try_double_delete(self, data):
    #     create_resp = self.api.create_item(data)
    #     item_id = create_resp.json().get('id')
    #     delete_resp1 = self.api.delete_item(item_id) if item_id else None
    #     delete_resp2 = self.api.delete_item(item_id) if item_id else None
    #     return delete_resp1, delete_resp2
    #
    # def unauthorized_operations(self, data, fake_id, headers=None):
    #     res_post = self.api.create_item_no_auth(data, headers)
    #     res_get = self.api.get_items_no_auth(headers=headers)
    #     res_put = self.api.update_item_no_auth(fake_id, data, headers)
    #     res_del = self.api.delete_item_no_auth(fake_id, headers)
    #     return res_post, res_get, res_put, res_del
