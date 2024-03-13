import asyncio
from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any, Tuple

import aiohttp
from bs4 import BeautifulSoup
from loguru import logger
from pydantic import BaseModel, HttpUrl

from models.article import Article


class NewsParserInterface(ABC):
    """
        Абстрактный класс для парсинга новостных сайтов.
    
        Атрибуты:
        - url (str): URL новостного сайта.
        - headers (Optional[Dict[str, str]]): Заголовки HTTP-запроса.
    
        Методы:
        - async fetch(session: aiohttp.ClientSession, url: str) -> str:  Асинхронное получение HTML-контента страницы.
        - async parse(session: aiohttp.ClientSession, url: str) -> List[Dict[str, Any]]: Абстрактный метод для парсинга страницы. Реализация в классах-наследниках.
        - async run() -> list[dict[str, Any]]: Запуск парсинга.
    """
    
    def __init__(self, url: str, headers: Optional[Dict[str, str]] = None):
        self.url = url
        self.headers = headers
    
    async def fetch(self, session: aiohttp.ClientSession, url: str) -> str:
        async with session.get(url, headers=self.headers) as response:
            return await response.text()
    
    @abstractmethod
    async def parse(self, session, url) -> List[Dict[str, Any]]:
        pass
    
    async def run(self) -> list[dict[str, Any]]:
        async with aiohttp.ClientSession() as session:
            result = await self.parse(session, self.url)
            return result


class KommersantParser(NewsParserInterface):
    """
        Парсер новостей с сайта Kommersant.
    
        Инициализация:
        - url (str): URL для парсинга.
        - headers (Optional[Dict[str, str]]): Заголовки HTTP-запроса.
    
        Методы:
        - async parse(session: aiohttp.ClientSession, url: str) -> List[Article]: Парсит страницу и возвращает список объектов Article.
    """
    
    def __init__(self, url: str, headers: Optional[Dict[str, str]] = None):
        super().__init__(url=url, headers=headers)
        self.source = "Kommersant"
    
    async def parse(self, session: aiohttp.ClientSession, url: str) -> List[Article]:
        html = await self.fetch(session, url)
        soup = BeautifulSoup(html, 'html.parser')
        articles_data = []
        articles = soup.find_all('article', class_={"uho", "rubric_lenta__item", "js-article"})
        for article in articles:
            try:
                title_element = article.find("span", class_={"vam"})
                timestamp_element = article.find("p", class_={"uho__tag", "rubric_lenta__item_tag", "hide_mobile"})
                relative_url_element = article.find("a",
                                                    class_={"uho__link",
                                                            "uho__link--overlay"},
                                                    attrs={"href": True})
                
                title = title_element.text.strip() if title_element else None
                timestamp = timestamp_element.text.strip() if timestamp_element else None
                article_url = "https://www.kommersant.ru" + relative_url_element.get(
                        "href") if relative_url_element else None
                article_data = Article(source=self.source,
                                       title=title,
                                       timestamp=timestamp,
                                       url=article_url)
                articles_data.append(article_data)
            except Exception as e:
                logger.error(f"Ошибка при обработке статьи: {e}")
        logger.info(f'Получено {len(articles_data)} статей с сайта: {url}')
        return articles_data


class RBCParser(NewsParserInterface):
    """
        Парсер новостей с сайта rbc.ru.
    
        Инициализация:
        - url (str): URL для парсинга.
        - headers (Optional[Dict[str, str]]): Заголовки HTTP-запроса.
    
        Методы:
        - async parse(session: aiohttp.ClientSession, url: str) -> List[Article]: Парсит страницу и возвращает список объектов Article.
    """
    
    def __init__(self, url: str, headers: Optional[Dict[str, str]] = None):
        super().__init__(url=url, headers=headers)
        self.source = "RBC"
    
    async def parse(self, session: aiohttp.ClientSession, url: str) -> List[Article]:
        html = await self.fetch(session, url)
        soup = BeautifulSoup(html, 'html.parser')
        articles_data = []
        articles = soup.find_all('div', class_={"item__wrap", "l-col-center"})
        for article in articles:
            try:
                title_element = article.find("span", class_="normal-wrap")
                timestamp_div = article.find("div", class_={"item__bottom"})
                timestamp_element = timestamp_div.find("span", class_={"item__category"}) if timestamp_div else None
                
                article_url = article.find('a',
                                           class_={"item__link", "rm-cm-item-link", "js-rm-central-column-item-link"},
                                           attrs={"href": True})
                
                title = title_element.text.strip() if title_element else None
                timestamp = timestamp_element.text.strip() if timestamp_element else None
                article_url = article_url.get('href') if article_url else None
                
                if title and timestamp and article_url:
                    article_data = Article(source=self.source,
                                           title=title,
                                           timestamp=timestamp,
                                           url=article_url)
                    articles_data.append(article_data)
            except Exception as e:
                logger.error(f"Ошибка при обработке статьи: {e}")
        logger.info(f'Получено {len(articles_data)} статей с сайта: {url}')
        return articles_data


class IXBTParser(NewsParserInterface):
    """
        Парсер новостей с сайта ixbt.com.
    
        Инициализация:
        - url (str): URL для парсинга.
        - headers (Optional[Dict[str, str]]): Заголовки HTTP-запроса.
    
        Методы:
        - async parse(session: aiohttp.ClientSession, url: str) -> List[Article]: Парсит страницу и возвращает список объектов Article.
    """
    
    def __init__(self, url: str, headers: Optional[Dict[str, str]] = None):
        super().__init__(url=url, headers=headers)
        self.source = "IXBT"
    
    async def parse(self, session, url) -> List[Article]:
        html = await self.fetch(session, url)
        soup = BeautifulSoup(html, 'html.parser')
        articles_data = []
        articles = soup.find_all('li', class_="item")
        for article in articles:
            try:
                title_element = article.find("a", class_={}, attrs={"href": True})
                timestamp_element = article.find("span", class_={"time_iteration_icon_light"})
                article_url = article.find("a", class_={"comments_link"}, attrs={"href": True})
                
                title = title_element.text.strip() if title_element else None
                timestamp = timestamp_element.text.strip() if timestamp_element else None
                article_url = "https://www.ixbt.com/" + article_url.get('href') if article_url else None
                
                if title and timestamp and article_url:
                    article_data = Article(source=self.source,
                                           title=title,
                                           timestamp=timestamp,
                                           url=article_url)
                    articles_data.append(article_data)
            except Exception as e:
                logger.error(f"Ошибка при обработке статьи: {e}")
        logger.info(f'Получено {len(articles_data)} статей с сайта: {url}')
        return articles_data


class RIAParser(NewsParserInterface):
    """
        Парсер новостей с сайта RIA новости.
    
        Инициализация:
        - url (str): URL для парсинга.
        - headers (Optional[Dict[str, str]]): Заголовки HTTP-запроса.
    
        Методы:
        - async parse(session: aiohttp.ClientSession, url: str) -> List[Article]: Парсит страницу и возвращает список объектов Article.
    """
    
    def __init__(self, url: str, headers: Optional[Dict[str, str]] = None):
        super().__init__(url=url, headers=headers)
        self.source = "RIA"
    
    async def parse(self, session, url) -> List[Article]:
        html = await self.fetch(session, url)
        soup = BeautifulSoup(html, 'html.parser')
        articles_data = []
        articles = soup.find_all('div', class_={"list-item"})
        for article in articles:
            try:
                title_element = article.find("a", class_={"list-item__title",
                                                          "color-font-hover-only"},
                                             attrs={"href": True})
                timestamp_element = article.find("div", class_={"list-item__date"})
                article_url = title_element.get('href') if title_element else None
                
                title = title_element.text.strip() if title_element else None
                timestamp = timestamp_element.text.strip() if timestamp_element else None
                if title and timestamp and article_url:
                    article_data = Article(source=self.source,
                                           title=title,
                                           timestamp=timestamp,
                                           url=article_url)
                    articles_data.append(article_data)
            except Exception as e:
                logger.error(f"Ошибка при обработке статьи: {e}")
        logger.info(f'Получено {len(articles_data)} статей с сайта: {url}')
        return articles_data


async def main() -> Tuple[Any]:
    import asyncio
    
    kommersant_parser = KommersantParser("https://www.kommersant.ru/hitech?from=burger")
    rbc_parser = RBCParser("https://www.rbc.ru/technology_and_media/?utm_source=topline")
    ixbt_parser = IXBTParser("https://www.ixbt.com/news/")
    ria_parser = RIAParser("https://ria.ru/technology/")
    
    tasks = [
        kommersant_parser.run(),
        rbc_parser.run(),
        ixbt_parser.run(),
        ria_parser.run()
    
    ]
    results = await asyncio.gather(*tasks)
    
    # Для отладки
    #
    # for result in results:
    #     for article in result:
    #         logger.info(
    #                 f"{article.source} - Заголовок: {article.title}, Время: {article.timestamp}, Ссылка: {article.url}")
    #
    
    return results


if __name__ == "__main__":
    asyncio.run(main())
