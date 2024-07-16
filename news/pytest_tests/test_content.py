import pytest

from django.conf import settings
from django.urls import reverse


# Количество новостей на главной странице — не более 10.
@pytest.mark.django_db
@pytest.mark.usefixtures('news_list')
def test_home_page_news_amount(client):
    url = reverse('news:home')
    response = client.get(url)
    object_list = response.context['object_list']
    news_amount = object_list.count()
    assert news_amount == settings.NEWS_COUNT_ON_HOME_PAGE


# Новости отсортированы от самой свежей к самой старой.
# Свежие новости в начале списка.
@pytest.mark.django_db
@pytest.mark.usefixtures('news_list')
def test_home_page_news_order(client):
    url = reverse('news:home')
    response = client.get(url)
    object_list = response.context['object_list']
    news_date_list = [news.date for news in object_list]
    sorted_date_list = sorted(news_date_list, reverse=True)
    assert sorted_date_list == news_date_list


# Комментарии на странице отдельной новости отсортированы
# от старых к новым: старые в начале списка, новые — в конце.
@pytest.mark.django_db
@pytest.mark.usefixtures('comment_list')
def test_news_comment_order(client, news):
    url = reverse('news:detail', args=(news.pk,))
    response = client.get(url)
    news = response.context['news']
    comments = news.comment_set.all()
    timestamps = [comment.created for comment in comments]
    sorted_timestamps = sorted(timestamps)
    assert timestamps == sorted_timestamps


# Анонимному пользователю недоступна форма для отправки комментария
# на странице отдельной новости, а авторизованному доступна.
@pytest.mark.parametrize(
    'user, expected_status',
    (
        (pytest.lazy_fixture('author_client'), True),
        (pytest.lazy_fixture('client'), False),
    ),
)
@pytest.mark.django_db
def test_client_form_availability(user, expected_status, news,):
    url = reverse('news:detail', args=(news.pk,))
    response = user.get(url)
    assert ('form' in response.context) == expected_status
