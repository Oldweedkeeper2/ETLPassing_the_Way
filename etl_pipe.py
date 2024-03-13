import asyncio
import json

from multi_parser import main as get_articles
from schemas.article import ArticleSchema


def save_to_json(data, filename='news_data.json'):
    """
    Сохраняет переданные данные в JSON файл.

    :param data: Данные для сохранения (список словарей).
    :param filename: Имя файла для сохранения данных.
    """
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


async def main():
    results = await get_articles()
    articles_list = []
    schema = ArticleSchema()
    for result in results:
        for article in result:
            article_dict = schema.dump(article)
            articles_list.append(article_dict)
    
    save_to_json(articles_list)


if __name__ == "__main__":
    asyncio.run(main())
