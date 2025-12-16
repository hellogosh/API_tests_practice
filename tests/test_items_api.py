import uuid
from httpx import Response
from src.item_models import ItemModel, ItemUpdateModel


class TestAPI:
    def test_create_and_delete_item(self, scenarios):
        """Тест создания и удаления элемента"""
        item_data = ItemModel.generate_random()
        create_resp, delete_resp = scenarios.create_and_delete_item(item_data)

        assert create_resp.id is not None
        assert create_resp.title == item_data.title
        assert delete_resp is True

    def test_create_and_update_item(self, scenarios):
        """Тест создания и обновления элемента"""
        item_data = ItemModel.generate_random()
        create_resp, update_resp = scenarios.create_and_update_item(item_data)

        assert create_resp.id is not None
        assert update_resp is not None
        if update_resp:
            assert '_updated' in update_resp.title

    def test_get_items_structure(self, scenarios):
        """Тест получения списка элементов"""
        items_list = scenarios.api.get_items()

        assert isinstance(items_list, list), (
            f"Ожидался list, получили {type(items_list)}"
        )

        if items_list:
            first_item = items_list[0]
            assert hasattr(first_item, 'id')
            assert hasattr(first_item, 'title')
            assert hasattr(first_item, 'description')

    def test_create_item_invalid_data(self, scenarios):
        """Тест создания элемента с невалидными данными"""
        invalid_cases = ItemModel.generate_invalid()

        for invalid_data in invalid_cases:
            response = scenarios.api.create_item(invalid_data)
            assert response.status_code in (400, 422)

    def test_negative_update_non_existent_item(self, scenarios):
        """Тест обновления несуществующего элемента"""
        fake_id = str(uuid.uuid4())
        payload = ItemUpdateModel.generate_full_update()
        response = scenarios.api.update_item(fake_id, payload)

        assert isinstance(response, Response)
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    def test_negative_try_double_delete(self, scenarios, created_item):
        """Тест двойного удаления элемента"""
        item_id = created_item.id

        del_resp1 = scenarios.api.delete_item(item_id)
        assert del_resp1 is True

        del_resp2 = scenarios.api.delete_item(item_id)
        assert del_resp2 is False or isinstance(del_resp2, Response)

    def test_negative_crud_ops_without_token(self, unauthorized_api):
        """Тест CRUD операций без авторизации"""
        fake_id = str(uuid.uuid4())
        update_data = ItemUpdateModel.generate_full_update()
        test_data = ItemModel.generate_random()

        create_resp = unauthorized_api.create_item(test_data)
        items_list = unauthorized_api.get_items()
        update_resp = unauthorized_api.update_item(fake_id, update_data)
        delete_resp = unauthorized_api.delete_item(fake_id)

        # Проверки create
        assert isinstance(create_resp, Response), (
            f"Создание должно вернуть Response, "
            f"получили {type(create_resp)}"
        )
        assert create_resp.status_code in (401, 403), (
            f"Создание: ожидали 401/403, "
            f"получили {create_resp.status_code}"
        )

        # Проверки get
        assert isinstance(items_list, Response), (
            f"Получение списка должно вернуть Response, "
            f"получили {type(items_list)}"
        )
        assert items_list.status_code in (401, 403), (
            f"Получение списка: ожидали 401/403, "
            f"получили {items_list.status_code}"
        )

        # Проверки update
        assert isinstance(update_resp, Response), (
            f"Обновление должно вернуть Response, "
            f"получили {type(update_resp)}"
        )
        assert update_resp.status_code in (401, 403), (
            f"Обновление: ожидали 401/403, "
            f"получили {update_resp.status_code}"
        )

        # Проверки delete
        assert isinstance(delete_resp, Response), (
            f"Удаление: ожидали Response при ошибке, "
            f"получили {type(delete_resp)}"
        )
        assert delete_resp.status_code in (401, 403), (
            f"Удаление: ожидали 401/403, "
            f"получили {delete_resp.status_code}"
        )