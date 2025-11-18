from pydantic import BaseModel
from typing import Optional
from faker import Faker

fake = Faker()


class Item(BaseModel):
    id: Optional[str] = None
    title: str
    description: str

    @classmethod
    def generate_valid(cls) -> dict:
        """Генерирует валидные данные для создания item"""
        return cls(
            title=fake.text(max_nb_chars=100).replace('\n', ' '),  # нормальный заголовок
            description=fake.text(max_nb_chars=500)  # нормальное описание
        ).model_dump()

    @classmethod
    def generate_invalid(cls) -> list[dict]:
        """Генерирует список невалидных данных для негативных тестов"""
        valid_data = cls.generate_valid()  # берем валидные данные как основу

        return [
            {**valid_data, "title": ""},  # пустой title
            {**valid_data, "title": "a" * 300},  # слишком длинный title
            {**valid_data, "description": "a" * 2000},  # слишком длинный description
            {**valid_data, "title": None},  # None вместо title
            {"description": valid_data["description"]},  # отсутствует title
            {},  # пустой объект
        ]

class ItemResponse(BaseModel):
    id: str
    title: str
    description: str


class ItemUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

    @classmethod
    def generate_full_update(cls) -> dict:
        """Генерирует данные для полного обновления (PUT)"""
        return cls(
            title=fake.text(max_nb_chars=100).replace('\n', ' '),
            description=fake.text(max_nb_chars=500)
        ).model_dump()

    @classmethod
    def generate_partial_update(cls) -> dict:
        """Генерирует данные для частичного обновления (PATCH)"""
        import random
        options = [
            {"title": fake.text(max_nb_chars=100).replace('\n', ' ')},
            {"description": fake.text(max_nb_chars=500)},
            {
                "title": fake.text(max_nb_chars=100).replace('\n', ' '),
                "description": fake.text(max_nb_chars=500)
            }
        ]
        return random.choice(options)