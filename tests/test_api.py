import requests
import pytest
from src.constant import Config
from src.models.data_models import ItemModel, ItemResponseModel, ItemUpdateModel
from src.utils import validate_response


class TestAPI:
    def test_create_and_delete_item(self, scenarios):
        """Тест создания и удаления элемента"""
        # Генерируем данные напрямую из модели
        item_data = ItemModel.generate_random()
        item = ItemModel(**item_data)

        create_resp, delete_resp = scenarios.create_and_delete_item(item)
        validate_response(create_resp, model=ItemResponseModel)
        assert delete_resp.status_code == 200

    def test_create_and_update_item(self, scenarios):
        """Тест создания и обновления элемента"""
        item_data = ItemModel.generate_random()
        item = ItemModel(**item_data)

        create_resp, update_resp = scenarios.create_and_update_item(item)
        validate_response(create_resp, model=ItemResponseModel)
        validate_response(update_resp, model=ItemResponseModel)
        assert update_resp.status_code == 200

    def test_get_items_structure(self, scenarios):
        """Тест получения списка элементов"""
        resp = scenarios.api.get_items()
        assert resp.status_code == 200, "Ошибка получения списка"

        items_data = resp.json()
        assert isinstance(items_data, dict), "Ответ должен быть объектом"
        assert "count" in items_data, "Ответ должен содержать поле count"
        assert "data" in items_data, "Ответ должен содержать поле data"
        assert isinstance(items_data["data"], list), "Поле data должно быть списком"

        if items_data["data"]:
            first_item = items_data["data"][0]
            assert "id" in first_item, "Элемент должен содержать id"
            assert "title" in first_item, "Элемент должен содержать title"
            assert "description" in first_item, "Элемент должен содержать description"

    def test_create_item_invalid_data(self, scenarios):
        """Тест создания элемента с невалидными данными"""
        # Генерируем невалидные данные напрямую из модели
        invalid_cases = ItemModel.generate_invalid()

        for invalid_data in invalid_cases:
            response = scenarios.api.create_item(invalid_data)
            assert response.status_code in (400, 422), "Ожидалась ошибка валидации"

    def test_negative_update_non_existent_item(self, scenarios):
        """Тест обновления несуществующего элемента"""
        fake_id = "99999999-9999-9999-9999-999999999999"

        # Генерируем данные для обновления из модели
        payload = ItemUpdateModel.generate_full_update()
        response = scenarios.api.update_item(fake_id, payload)

        assert response.status_code in (404, 422), "Ожидалась ошибка 'не найден'"

    def test_negative_try_double_delete(self, scenarios, created_item):
        """Тест двойного удаления элемента"""
        # Используем фикстуру created_item вместо создания нового
        item_id = created_item["id"]

        # Первое удаление
        del_resp1 = scenarios.api.delete_item(item_id)
        assert del_resp1.status_code == 200, "Первое удаление должно быть успешным"

        # Второе удаление
        del_resp2 = scenarios.api.delete_item(item_id)
        assert del_resp2.status_code in (404, 400), "Второе удаление должно вернуть ошибку"

    def test_negative_crud_ops_without_token(self):
        """Тест CRUD операций без авторизации"""
        headers = {'Content-Type': 'application/json'}
        fake_id = "12345678-1234-1234-1234-123456789012"

        # Генерируем тестовые данные из модели
        test_data = ItemModel.generate_random()

        # Создание без авторизации
        res_post = requests.post(f'{Config.BASE_URL}items/', json=test_data, headers=headers)
        # Получение списка без авторизации
        res_get = requests.get(f'{Config.BASE_URL}items/', headers=headers)
        # Обновление без авторизации
        res_put = requests.put(f'{Config.BASE_URL}items/{fake_id}', json=test_data, headers=headers)
        # Удаление без авторизации
        res_del = requests.delete(f'{Config.BASE_URL}items/{fake_id}', headers=headers)

        assert res_post.status_code in (401, 403), "Создание без авторизации должно быть запрещено"
        assert res_get.status_code in (401, 403), "Получение без авторизации должно быть запрещено"
        assert res_put.status_code in (401, 403), "Обновление без авторизации должно быть запрещено"
        assert res_del.status_code in (401, 403), "Удаление без авторизации должно быть запрещено"