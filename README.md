# ETL Конвейер для Новостных Сайтов

Этот проект представляет собой мою первую попытку создать ETL (Extract, Transform, Load) конвейер для извлечения
новостей с различных новостных сайтов, их трансформации и сохранения в JSON файлике. Проект написан на Python и
использует асинхронность для парсинга.

## Основные Компоненты

Проект состоит из следующих основных компонентов:

- **Парсеры новостей**: Классы для извлечения данных с конкретных новостных сайтов.
- **Модель данных**: Определение структуры данных для новостей.
- **ETL конвейер**: Интеграция процессов извлечения, трансформации и загрузки данных.

## Используемые Библиотеки

- `aiohttp` для асинхронных HTTP запросов.
- `BeautifulSoup` для парсинга HTML.
- `marshmallow` для сериализации и валидации данных.
- `pytest` и `pytest-asyncio` для тестирования.

## Установка Зависимостей

Для установки необходимых библиотек выполните следующую команду:

```bash
pip install aiohttp beautifulsoup4 marshmallow pytest pytest-asyncio
```

## Структура Проекта

Проект организован следующим образом:

    parsers/: Директория с классами парсеров для каждого новостного сайта.
    models.py: Определения моделей данных.
    etl.py: Основной скрипт ETL конвейера.
    tests/: Директория с тестами для парсеров.

## Запуск Тестов

Для запуска тестов используйте команду pytest в корневой директории проекта:

```bash
pytest
```

Убедитесь, что все тесты успешно проходят, прежде чем использовать ETL конвейер в проде.

## Как Использовать

Для запуска ETL конвейера выполните скрипт etl.py:

```bash
python etl.py
```

Результаты работы конвейера будут сохранены в файл news_data.json.

## Вклад в Проект

Если у вас есть предложения по улучшению моих навыков или кода, то не стесняйтесь создавать issue или pull request.

### Контакты

TG: @Oldweedkeeper