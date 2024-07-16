from datetime import datetime, timedelta
import pytest

from django.conf import settings
from django.contrib.auth import get_user_model
from django.test.client import Client
from django.utils import timezone

from news.forms import BAD_WORDS
from news.models import Comment, News


User = get_user_model()

TEXT = 'Some text'
NEW_TEXT = 'Another text'
TITLE = 'News title'
NEW_TITLE = 'Another title'
COMMENT = 'Comment'
NEW_COMMENT = 'New Comment'
COMMENT_AMOUNT = 13

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
        text=TEXT
    )
    return news


@pytest.fixture
def comment(author, news):
    comment = Comment.objects.create(
        news=news,
        author=author,
        text=TEXT
    )
    return comment


@pytest.fixture
def news_list():
    news_list = News.objects.bulk_create(
        News(
            title=f'{TITLE} #{i}',
            text=f'{TEXT} of {TITLE} #{i}',
            date=datetime.today() - timedelta(days=i)
        )
        for i in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    )
    return news_list


@pytest.fixture
def comment_list(news, author):
    now = timezone.now()

    for i in range(COMMENT_AMOUNT):
        comment = Comment.objects.create(
            news=news,
            author=author,
            text=f'{COMMENT} #{i}'
        )
        comment.created = now + timedelta(hours=i)
        comment.save


@pytest.fixture
def comment_form_data():
    return {
        'text': NEW_COMMENT,
    }


@pytest.fixture
def swear_word_data():
    return {'text': f'{TEXT}, {BAD_WORDS[0]}'}
