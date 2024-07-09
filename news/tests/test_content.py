from django.conf import settings
from django.test import TestCase

from news.models import News


class TestContent(TestCase):

    # фикстуры: нужно создать более десятка новостей, тогда можно будет понять,
    # ограничивается ли их количество при выводе на главную.
    # Количество новостей, выводимых на страницу указывается в настройках
    # settings.NEWS_COUNT_ON_HOME_PAGE, поэтому для тестов создадим
    # (settings.NEWS_COUNT_ON_HOME_PAGE + 1) новостей, чтобы их было заведомо
    # больше, чем должно отобразиться на странице.
    # Первое же решение, которое приходит на ум — создать цикл
    # и на каждой итерации цикла создавать объекты.
    @classmethod
    def setUpTestData(cls):
        for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1):
            News.objects.create(title=f'Новость {index}', text='Просто текст.')
    # На каждой итерации будет отправляться запрос к БД.
    # Это как минимум неэффективно
    # Для одновременного создания нескольких объектов применяют метод
    # bulk_create()
    
