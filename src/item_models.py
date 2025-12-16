from pydantic import BaseModel
from typing import Optional
from faker import Faker

fake = Faker()


class ItemModel(BaseModel):
    id: Optional[str] = None
    title: str
    description: str


    @classmethod
    def generate_valid(cls) -> "ItemModel":
        """Генерирует валидные данные для создания item"""
        return cls(
            title=fake.text(max_nb_chars=50).replace('\n', ' '),
            description=fake.text(max_nb_chars=200)
        )


    @classmethod
    def generate_random(cls) -> "ItemModel":
        """Генерирует случайные тестовые данные"""
        return cls(
            title=fake.word().capitalize(),
            description=fake.sentence(nb_words=8)
        )


    @classmethod
    def generate_invalid(cls) -> list[dict]:
        """Генерирует список невалидных данных"""
        valid_data = cls.generate_valid().model_dump()
        return [
            {**valid_data, "title": ""},
            {**valid_data, "title": "a" * 256},
            {**valid_data, "description": "a" * 256},
            {**valid_data, "title": None},
            {"description": valid_data["description"]},
            {},
        ]


class ItemResponseModel(BaseModel):
    id: str
    title: str
    description: Optional[str] = None


class ItemUpdateModel(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None


    @classmethod
    def generate_full_update(cls) -> dict:
        """Генерирует данные для полного обновления"""
        return cls(
            title=fake.text(max_nb_chars=50).replace('\n', ' '),
            description=fake.text(max_nb_chars=200)
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