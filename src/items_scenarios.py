from typing import Tuple, Optional
from src.items_client import ItemsApiClient
from src.item_models import ItemModel, ItemResponseModel


class ItemScenarios:
    def __init__(self, api_client: ItemsApiClient):
        self.api = api_client

    def create_and_delete_item(self, item_data: ItemModel) -> Tuple[ItemResponseModel, bool]:
        create_item = self.api.create_item(item_data)

        item_id = create_item.id
        if not item_id:
            return create_item, False

        deleted = self.api.delete_item(item_id)

        return create_item, deleted


    def create_and_update_item(self, item_data: ItemModel,
                               upd_suffix: str ='_updated') -> Tuple[ItemResponseModel, Optional[ItemResponseModel]]:
        create_item = self.api.create_item(item_data)

        if not create_item.id:
            return create_item, None

        updated_data = ItemModel(
            title=f'{item_data.title}{upd_suffix}',
            description=f'{item_data.description} updated'
        )

        updated_item = self.api.update_item(create_item.id, updated_data)

        return create_item, updated_item

    def create_temp_item(self) -> ItemResponseModel:
        item_data = ItemModel.generate_valid()
        return self.api.create_item(item_data)

    def cleanup_item(self, item_id: str) -> bool:
        return self.api.delete_item(item_id)

    def full_crud_flow(self) -> dict:
        results = {}

        item_data = ItemModel.generate_random()
        results['created'] = self.api.create_item(item_data)

        results['read'] =self.api.get_item(results['created'].id)

        updated_data = ItemModel (
            title=f'{item_data.title}_modified',
            description='Modified via full CRUD flow'
        )
        results['updated'] = self.api.update_item(
            results['created'].id,
            updated_data
        )

        results['deleted'] = self.api.delete_item(results['created'].id)

        return results

    def bulk_create_and_validate(self, count: int = 3) -> list[ItemResponseModel]:

        created_items = []

        for i in range(count):
            item_data = ItemModel(
                title=f'Test Item {i + 1}',
                description=f'Description for item {i + 1}'
            )

            item = self.api.create_item(item_data)
            created_items.append(item)

            assert item.id is not None, f"Item {i + 1} не получил ID"
            assert item.title == item_data.title, f"Неправильный title у item {i + 1}"

        return created_items