import uuid

from config.constant import Config
from models.item_models import ItemModel, ItemResponseModel, ItemUpdateModel
from api.items_client import ItemsApiClient
from requests import Response

class TestAPI:
    def test_create_and_delete_item(self, scenarios):
        """Тест создания и удаления элемента"""
        # Генерируем данные напрямую из модели
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

            assert isinstance(items_list, list), f"Ожидался list, получили {type(items_list)}"

            if items_list:
                first_item = items_list[0]
                assert hasattr(first_item, 'id'), "Элемент должен содержать id"
                assert hasattr(first_item, 'title'), "Элемент должен содержать title"
                assert hasattr(first_item, 'description'), "Элемент должен содержать description"


    def test_create_item_invalid_data(self, scenarios):
        """Тест создания элемента с невалидными данными"""
        # Генерируем невалидные данные напрямую из модели
        invalid_cases = ItemModel.generate_invalid()

        for invalid_data in invalid_cases:
            response = scenarios.api.create_item(invalid_data)
            assert response.status_code in (400, 422), "Ожидалась ошибка валидации"

    def test_negative_update_non_existent_item(self, scenarios):
        """Тест обновления несуществующего элемента"""
        fake_id = str(uuid.uuid4())
        payload = ItemUpdateModel.generate_full_update()

        response = scenarios.api.update_item(fake_id, payload)

        assert isinstance(response, Response), "Должен вернуть Response объект"
        assert response.status_code == 404, f"Ожидали 404, получили {response.status_code}"
        assert "not found" in response.json()["detail"].lower()

    def test_negative_try_double_delete(self, scenarios, created_item):
        """Тест двойного удаления элемента"""
        # Используем фикстуру created_item вместо создания нового
        item_id = created_item.id

        # Первое удаление
        del_resp1 = scenarios.api.delete_item(item_id)
        assert del_resp1 is True, "Первое удаление должно быть успешным"

        # Второе удаление
        del_resp2 = scenarios.api.delete_item(item_id)
        assert del_resp2 is False or isinstance(del_resp2, Response)

    def test_negative_crud_ops_without_token(self, unauthorized_api):
        """Тест CRUD операций без авторизации"""
        # Теперь используем новый unauthorized_api

        fake_id = str(uuid.uuid4())
        update_data = ItemUpdateModel.generate_full_update()
        test_data = ItemModel.generate_random()

        create_resp = unauthorized_api.create_item(test_data)
        items_list = unauthorized_api.get_items()
        update_resp = unauthorized_api.update_item(fake_id, update_data)
        delete_resp = unauthorized_api.delete_item(fake_id)

        assert isinstance(create_resp, Response) and create_resp.status_code in (401, 403), "Создание без токена должно вернуть 401/403"
        assert isinstance(items_list, Response) and items_list.status_code in (401, 403), "Получение списка без токена должно вернуть 401/403"
        assert isinstance(update_resp, Response) and update_resp.status_code in (401, 403), "Обновление без токена должно вернуть 401/403"
        assert not delete_resp, "Удаление без токена должно вернуть False"
