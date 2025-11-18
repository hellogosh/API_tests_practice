import requests
import pytest
from src.constant import Config
from models.data_models import Item, ItemResponse
from src.utils import validate_response

BASE_URL = Config.BASE_URL

class TestAPI:
    def test_create_and_delete_item(self, scenarios, item_data):
        """Тест создания и удаления элемента"""
        item = Item(**item_data)
        create_resp, delete_resp = scenarios.create_and_delete_item(item)

        # Валидируем ответ создания
        validate_response(create_resp, model=ItemResponse)

        # Проверяем удаление
        assert delete_resp is not None and delete_resp.status_code == 200

    def test_create_and_update_item(self, scenarios, item_data):
        """Тест создания и обновления элемента"""
        item = Item(**item_data)
        create_resp, update_resp = scenarios.create_and_update_item(item)

        # Валидируем оба ответа
        validate_response(create_resp, model=ItemResponse)
        validate_response(update_resp, model=ItemResponse)

        # Проверяем, что обновление прошло успешно
        assert update_resp.status_code == 200

    def test_get_items_structure(self, scenarios):
        """Тест получения списка элементов"""
        resp = scenarios.api.get_items()
        assert resp.status_code == 200, "Ошибка получения списка"

        # Валидируем структуру ответа
        try:
            items_data = resp.json()
            # API возвращает объект с полями count и data
            assert isinstance(items_data, dict), "Ответ должен быть объектом"
            assert "count" in items_data, "Ответ должен содержать поле count"
            assert "data" in items_data, "Ответ должен содержать поле data"
            assert isinstance(items_data["data"], list), "Поле data должно быть списком"

            # Дополнительная проверка: если есть элементы, проверяем их структуру
            if items_data["data"]:
                first_item = items_data["data"][0]
                assert "id" in first_item, "Элемент должен содержать id"
                assert "title" in first_item, "Элемент должен содержать title"
                assert "description" in first_item, "Элемент должен содержать description"

        except ValueError:
            pytest.fail("Невалидный JSON в ответе")

    def test_create_item_invalid_data(self, scenarios, invalid_payload):
        for invalid_data in invalid_payload:
            response = scenarios.api.create_item(invalid_data)
            assert response.status_code in (400, 422), "Ожидалась ошибка валидации"

    def test_negative_update_non_existent_item(self, scenarios):
        """Тест обновления несуществующего элемента"""
        fake_id = "99999999-9999-9999-9999-999999999999"
        payload = {"title": "test", "description": "test"}
        response = scenarios.api.update_item(fake_id, payload)
        assert response.status_code in (404, 422), "Ожидалась ошибка 'не найден'"

    def test_negative_try_double_delete(self, scenarios, item_data):
        """Тест двойного удаления элемента"""
        item = Item(**item_data)
        create_resp, del_resp1 = scenarios.create_and_delete_item(item)

        # Валидируем создание
        validate_response(create_resp, model=ItemResponse)

        # Получаем ID созданного элемента
        item_id = create_resp.json().get('id')
        assert item_id is not None, "ID элемента не должен быть None"

        # Первое удаление должно быть успешным
        assert del_resp1.status_code == 200, "Первое удаление должно быть успешным"

        # Второе удаление должно вернуть ошибку
        del_resp2 = scenarios.api.delete_item(item_id)
        assert del_resp2.status_code in (404, 400), "Второе удаление должно вернуть ошибку"

    def test_negative_crud_ops_without_token(self, item_data):
        """Тест CRUD операций без авторизации"""
        headers = {'Content-Type': 'application/json'}
        fake_id = "12345678-1234-1234-1234-123456789012"  # Строковый UUID

        # Создание без авторизации
        res_post = requests.post(f'{BASE_URL}items/', json=item_data, headers=headers)

        # Получение списка без авторизации
        res_get = requests.get(f'{BASE_URL}items/', headers=headers)

        # Обновление без авторизации
        res_put = requests.put(f'{BASE_URL}items/{fake_id}', json=item_data, headers=headers)

        # Удаление без авторизации
        res_del = requests.delete(f'{BASE_URL}items/{fake_id}', headers=headers)

        # Проверяем, что все операции без авторизации возвращают ошибку
        assert res_post.status_code in (401, 403), "Создание без авторизации должно быть запрещено"
        assert res_get.status_code in (401, 403), "Получение без авторизации должно быть запрещено"
        assert res_put.status_code in (401, 403), "Обновление без авторизации должно быть запрещено"
        assert res_del.status_code in (401, 403), "Удаление без авторизации должно быть запрещено"