import pytest

from django.contrib.auth import get_user_model
from django.test.client import Client

from news.models import Comment, News


User = get_user_model()

SOME_TEXT = 'Some news text'
TITLE = 'News title'


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Author')


@pytest.fixture
def not_author(django_user_model):
    return django_user_model.objects.create(username='Not author')


@pytest.fixture
def author_client(author):
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def not_author_client(not_author):
    client = Client()
    client.force_login(not_author)
    return client


@pytest.fixture
def news():
    news = News.objects.create(
        title=TITLE,
        text=SOME_TEXT
    )
    return news


@pytest.fixture
def comment(author, news):
    comment = Comment.objects.create(
        news=news,
        author=author,
        text=SOME_TEXT
    )
    return comment
    
