import aiohttp
import pytest


@pytest.mark.asyncio
async def test_site_connection():
    """
        Проверка подключения к сайтам.
        :return: None
    """
    urls = [
        "https://www.kommersant.ru/hitech?from=burger",
        "https://www.rbc.ru/technology_and_media/?utm_source=topline",
        "https://www.ixbt.com/news/",
        "https://ria.ru/technology/"
    ]
    
    async with aiohttp.ClientSession() as session:
        for url in urls:
            try:
                async with session.get(url) as response:
                    assert response.status == 200, f"Не удалось подключиться к {url}. Код ответа: {response.status}"
                    print(f"Подключение прошло успешно: {url}. Код ответа: {response.status}")
            except aiohttp.ClientError as e:
                pytest.fail(f"Ошибка клиента при попытке подключения к {url}: {str(e)}")
            except Exception as e:
                pytest.fail(f"Ошибка при попытке подключения к {url}: {str(e)}")
