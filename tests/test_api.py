import requests
import pytest
from config.constant import BASE_URL

class Test_API:
    endpoint = f'{BASE_URL}items/'

    def test_create_new_item(self, auth_session, item_data):  # создание нового item
        response = auth_session.post(self.endpoint, json=item_data)
        assert response.status_code == 200, "ошибка создания item"

    def test_get_items(self, auth_session):  # получение списка элементов, проверка структуры ответа (`count`,`data`)
        response = auth_session.get(self.endpoint)
        assert response.status_code == 200, "ошибка получения списка"
        response_json = response.json()
        assert 'count' in response_json, "отсутствует count"
        assert 'data' in response_json, "отсутствует data"

    def test_filter_items(self, auth_session, item_data):
        fixed_item = {
            "title": "test_filter_title",  # фиксированное значение для фильтрации
            "description": "test_filter_description"
        }
        response = auth_session.post(self.endpoint, json=fixed_item)
        assert response.status_code == 200, "Не удалось создать элемент для фильтрации"
        created_item = response.json()

        params = {"title": fixed_item["title"]}
        response = auth_session.get(self.endpoint, params=params)
        assert response.status_code == 200, "Ошибка запроса с фильтром по title"
        data = response.json().get('data', [])
        assert any(item['id'] == created_item['id'] for item in data), \
            "Созданный элемент не найден в результате фильтрации по title"

        params = {"description": "example"}
        response = auth_session.get(self.endpoint, params=params)
        assert response.status_code == 200, "Ошибка запроса с фильтром по description"
        data = response.json().get('data', [])
        assert any(item['id'] == created_item['id'] for item in data), \
            "Созданный элемент не найден в результате фильтрации по description"

    def test_pagination_items(self, auth_session):
        limit = 5
        params = {"limit": limit}
        response = auth_session.get(self.endpoint, params=params)
        assert response.status_code == 200, f"Ошибка пагинации, статус {response.status_code}"
        data = response.json().get('data', [])
        assert len(data) <= limit

        params_skip = {"limit": limit, "skip": limit}
        response_skip = auth_session.get(self.endpoint, params=params_skip)
        assert response_skip.status_code == 200
        data_skip = response_skip.json().get('data', [])
        assert data != data_skip

    def test_update_item(self, auth_session, item_data):
        response = auth_session.post(self.endpoint, json=item_data)
        assert response.status_code == 200, f'Ошибка создания {response.status_code}'

        id_num = response.json().get('id')
        assert id_num is not None, "ID не получен после создания"

        original_data = response.json()
        print("Исходные данные:", original_data)

        updated_data = item_data.copy()
        updated_data['title'] = updated_data.get('title', '') + "_updated"
        updated_data['description'] = updated_data.get('description', '') + " updated"

        update_url = f"{self.endpoint.rstrip('/')}/{id_num}"

        headers = auth_session.headers.copy()
        headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json",
        })

        update_response = auth_session.put(update_url, json=updated_data, headers=headers)
        print("PUT URL:", update_url)
        print("PUT статус:", update_response.status_code)
        print("PUT response:", update_response.text)

        assert update_response.status_code == 200, f'Ошибка обновления: {update_response.status_code}'

        new_data = update_response.json()
        assert new_data != original_data, "обновление неуспешно"
        assert new_data.get('title') == updated_data['title'], "Поле title не обновлено"
        assert new_data.get('description') == updated_data['description'], "Поле description не обновлено"

        print("Данные после обновления:", new_data)

    def test_delete_item(self, auth_session, item_data):
        response = auth_session.post(url=self.endpoint, json=item_data)
        response_id = response.json().get('id')
        print(response_id)
        del_item = auth_session.delete(url=f"{self.endpoint.rstrip('/')}/{response_id}")
        assert del_item.status_code == 200, "ошибка удаления"

    @pytest.mark.parametrize("invalid_payload", [
        {"title": "", "description": "valid description"},
        {"title": "a" * 300, "description": "desc"},
        {"title": "valid", "description": "a" * 2000},
        {"title": None, "description": "desc"},
        {"description": "desc only"},
    ])
    def test_create_item_invalid_data(self, auth_session, invalid_payload):
        response = auth_session.post(self.endpoint, json=invalid_payload)
        assert response.status_code in (400, 422), \
            f"Ожидается ошибка валидации для {invalid_payload}, получен {response.status_code}"
        error_detail = response.json().get("detail", "")
        print(f"Ошибка для данных {invalid_payload}: {error_detail}")

    def test_negative_crud_ops_without_token(self):
        headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
        response_post = requests.post(self.endpoint, headers=headers, json={"title": "test", "description": "desc"})
        assert response_post.status_code in (401, 403),\
            f"Ожидается ошибка авторизации, получен {response_post.status_code}"

        response_get = requests.get(self.endpoint, headers=headers, json={"title": "test", "description": "desc"})
        assert response_get.status_code in (401, 403), \
            f'Ожидается ошибка получения item, получен {response_get.status_code}'

        fake_id = "123"
        response_delete = requests.delete(url=f"{self.endpoint.rstrip('/')}/{fake_id}")
        assert response_delete.status_code in (401, 403), \
            f"Ожидается ошибка удаления, получен {response_delete.status_code}"

        put_payload = {"title": "update title", "description": "update description"}
        response_put = requests.put(f"{self.endpoint.rstrip('/')}/{fake_id}", headers=headers, json=put_payload)
        assert response_put.status_code in (401, 403), \
            f"Ожидается ошибка обновления, получен {response_put.status_code}"

    def test_negative_update_non_existent_item(self, auth_session):
        fake_id = "123"
        update_url = f'{self.endpoint.rstrip("/")}/{fake_id}'
        payload = {"title": "test", "description": "test"}

        response = auth_session.put(update_url, json=payload)
        assert response.status_code == 422, \
            f'Ожидается ошибка обновления несуществующего элемента, получен {response.status_code}'

    def test_negative_try_double_delete(self, auth_session, item_data):
        response = auth_session.post(url=self.endpoint, json=item_data)
        response_id = response.json().get('id')

        del_item = auth_session.delete(url=f"{self.endpoint.rstrip('/')}/{response_id}")
        assert del_item.status_code == 200, "ошибка удаления"

        double_del = auth_session.delete(url=f"{self.endpoint.rstrip('/')}/{response_id}")
        assert double_del.status_code == 404, 'совершилось двойное удаление'
