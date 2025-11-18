# API Tests Practice

Проект содержит автоматические тесты для проверки CRUD-операций API ресурсов.

**Тестируемое API:** https://dashboard.fast-api.senior-pomidorov.ru/

## Что проверяет

- ✅ **Создание** нового элемента
- ✅ **Получение** списка элементов (структура, фильтрация, пагинация)
- ✅ **Полное обновление** элемента по ID
- ✅ **Удаление** элемента по ID
- ✅ Обработка ошибок (несуществующие элементы, запросы без токена)

## Быстрый старт

### Предварительные требования

- Python 3.9 или новее
- Git

### Установка и запуск

```bash
# 1. Клонируйте репозиторий
git clone https://github.com/hellogosh/API_tests_practice.git

# 2. Перейдите в директорию проекта
cd API_tests_practice

# 3. Создайте виртуальное окружение
python -m venv venv

# 4. Активируйте виртуальное окружение
# Для Linux/macOS:
source venv/bin/activate
# Для Windows:
venv\Scripts\activate

# 5. Установите зависимости
pip install -r requirements.txt

# 6. Настройте конфигурацию
# Отредактируйте файл config/constant.py, указав:
# - BASE_URL вашего API
# - Другие параметры доступа

# 7. Запустите тесты
pytest -s
```
## Структура проекта

```
API_tests_practice/
├── tests/               # Тестовые модули
├── config/
│   └── constant.py     # Настройки и константы
├── requirements.txt    # Зависимости
└── README.md          # Этот файл
```

## Контакты

По вопросам и предложениям обращайтесь: [@pantyukhovsky](https://t.me/pantyukhovsky)
