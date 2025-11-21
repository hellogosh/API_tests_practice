from pydantic import BaseModel
from typing import Optional
from faker import Faker

fake = Faker()


class ItemModel(BaseModel):
    id: Optional[str] = None
    title: str
    description: str


    @classmethod
    def generate_valid(cls) -> dict:
        """Генерирует валидные данные для создания item"""
        return cls(
            title=fake.text(max_nb_chars=50).replace('\n', ' '),  # 👈 Уменьшил до 50
            description=fake.text(max_nb_chars=200)  # 👈 Уменьшил до 200
        ).model_dump()


    @classmethod
    def generate_random(cls) -> dict:
        """Генерирует случайные тестовые данные"""
        return {
            "title": fake.word().capitalize(),
            "description": fake.sentence(nb_words=8)  # 👈 Короткое описание
        }


    @classmethod
    def generate_invalid(cls) -> list[dict]:
        """Генерирует список невалидных данных"""
        valid_data = cls.generate_valid()

        return [
            {**valid_data, "title": ""},
            {**valid_data, "title": "a" * 256},  # 👈 256 символов (>255)
            {**valid_data, "description": "a" * 256},  # 👈 256 символов (>255)
            {**valid_data, "title": None},
            {"description": valid_data["description"]},
            {},
        ]


class ItemResponseModel(BaseModel):
    id: str
    title: str
    description: str


class ItemUpdateModel(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None


    @classmethod
    def generate_full_update(cls) -> dict:
        """Генерирует данные для полного обновления"""
        return cls(
            title=fake.text(max_nb_chars=50).replace('\n', ' '),  # 👈 Уменьшил
            description=fake.text(max_nb_chars=200)  # 👈 Уменьшил
        ).model_dump()


    @classmethod
    def generate_partial_update(cls) -> dict:
        """Генерирует данные для частичного обновления"""
        import random
        options = [
            {"title": fake.text(max_nb_chars=50).replace('\n', ' ')},  # 👈 Уменьшил
            {"description": fake.text(max_nb_chars=200)},  # 👈 Уменьшил
            {
                "title": fake.text(max_nb_chars=50).replace('\n', ' '),
                "description": fake.text(max_nb_chars=200)
            }
        ]
        return random.choice(options)