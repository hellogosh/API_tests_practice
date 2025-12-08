# API Tests Practice

Автоматизированные тесты API для CRUD операций с комплексной валидацией.

## Быстрый старт

### 1. Клонирование и настройка

Клонируйте репозиторий:
```bash
git clone https://github.com/hellogosh/API_tests_practice.git
```
Перейдите в директорию проекта:
```bash
cd API_tests_practice
```
Создайте виртуальное окружение:

```bash
python -m venv venv
```
Активируйте виртуальное окружение:

Для Linux/macOS:

```bash
source venv/bin/activate
```
Для Windows:

```bash
venv\Scripts\activate
```
Установите зависимости:

```bash
pip install -r requirements.txt
```

### 2. Настройка окружения:

Скопируйте файл окружения:
```bash
cp .env.example .env
```
Отредактируйте файл .env и укажите ваши учетные данные:

env
API_USERNAME=your_test_username
API_PASSWORD=your_test_password


### 3. Запуск тестов
Запустите все тесты:
```bash
pytest -v
```
### Структура проекта
```

tests/              # Тестовые сценарии
src/                # API клиенты и утилиты  
models/             # Модели данных и фабрики
config/             # Конфигурационные файлы
```
### Покрытие тестами

✅ CRUD операции (Создание, Чтение, Обновление, Удаление)

✅ Валидация данных и обработка ошибок

✅ Аутентификация и авторизация

✅ Пагинация и фильтрация

### Нужна помощь?
Напишите: @pantyukhovsky