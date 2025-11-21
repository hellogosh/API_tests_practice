# API Tests Practice

Автоматизированные тесты API для CRUD операций с комплексной валидацией.

## Быстрый старт

### 1. Клонирование и настройка
```bash
git clone https://github.com/hellogosh/API_tests_practice.git
cd API_tests_practice
python -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate   # Windows
pip install -r requirements.txt

2. Настройка окружения
bash
# Скопируйте и отредактируйте .env файл
cp .env.example .env
Отредактируйте файл .env:

env
API_USERNAME=your_test_username
API_PASSWORD=your_test_password

3. Запуск тестов
bash
pytest -v

Структура проекта
text
tests/              # Тестовые сценарии
src/                # API клиенты и утилиты  
models/             # Модели данных и фабрики
config/             # Конфигурационные файлы

Покрытие тестами
✅ CRUD операции (Создание, Чтение, Обновление, Удаление)

✅ Валидация данных и обработка ошибок

✅ Аутентификация и авторизация

✅ Пагинация и фильтрация

Расширенное использование
bash
# Запуск с детальным отчетом
pytest -v --html=report.html

# Запуск конкретного теста
pytest tests/test_api.py::TestAPI::test_create_item

Нужна помощь?
Напишите: @pantyukhovsky