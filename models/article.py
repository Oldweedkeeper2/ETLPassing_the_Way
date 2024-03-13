from typing import Optional, Dict, Any

from pydantic import BaseModel, HttpUrl


class Article(BaseModel):
    """
        Модель для хранения базовой информации о новостях.

        Атрибуты:
        - source (str): Источник новости.
        - title (str): Заголовок новости.
        - timestamp (Optional[str]): Время публикации новости. Может быть None.
        - url (HttpUrl): Ссылка на новость.

        Методы:
        - dict(*args, **kwargs) -> Dict[str, Any]: Возвращает словарь с данными новости.
    """
    source: str
    title: str
    timestamp: Optional[str] = None
    url: HttpUrl
    
    def dict(self, *args, **kwargs) -> Dict[str, Any]:
        return {"source": self.source, "title": self.title, "timestamp": self.timestamp, "url": self.url}
