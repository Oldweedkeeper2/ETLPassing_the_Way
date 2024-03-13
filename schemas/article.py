from marshmallow import Schema, fields, post_load

from models.article import Article


class ArticleSchema(Schema):
    """
        Схема для сериализации и десериализации модели Article.
        
        Атрибуты:
        - source (str): Источник новости.
        - title (str): Заголовок новости.
        - timestamp (Optional[str]): Время публикации новости. Может быть None.
        - url (HttpUrl): Ссылка на новость.
        
        Методы:
        - make_article(self, data, **kwargs): Создает модель Article.
    """
    source = fields.Str()
    title = fields.Str()
    timestamp = fields.Str(allow_none=True)
    url = fields.Url()
    
    @post_load
    def make_article(self, data, **kwargs):
        return Article(**data)
