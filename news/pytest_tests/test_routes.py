from http import HTTPStatus

import pytest
from pytest_django.asserts import assertRedirects


from django.urls import reverse


# Не понял: почему тут нужно использовать маркер django_db
# В примерах из лекций по YaNote прекрасно работало без всяких маркеров.

@pytest.mark.parametrize(
    'url_name',
    ('news:home', 'users:login', 'users:logout', 'users:signup')
)
@pytest.mark.django_db
def test_home_page_availability_for_anonymous_user(client, url_name):
    url = reverse(url_name)
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


# Страница отдельной новости доступна анонимному пользователю.
@pytest.mark.django_db
def test_detail_page_availability_for_anonimous_user(client, news):
    url = reverse('news:detail', args=(news.pk,))
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


# Страницы удаления и редактирования комментария
# доступны автору комментария.
@pytest.mark.parametrize(
    'parametrized_client, expected_status',
    (
        (pytest.lazy_fixture('author_client'), HTTPStatus.OK),
        (pytest.lazy_fixture('not_author_client'), HTTPStatus.NOT_FOUND),
    ),
)
@pytest.mark.parametrize(
    'url_name',
    ('news:edit', 'news:delete')
)
@pytest.mark.django_db
def test_availability_for_comment_edit_and_delete(
    parametrized_client, expected_status, url_name, comment,
):
    url = reverse(url_name, args=(comment.pk,))
    response = parametrized_client.get(url)
    assert response.status_code == expected_status


# При попытке перейти на страницу редактирования или удаления комментария
# анонимный пользователь перенаправляется на страницу авторизации.
@pytest.mark.parametrize(
    'url_name',
    ('news:edit', 'news:delete')
)
def test_redirect_for_anonymous_client(client, url_name, comment):
    login_url = reverse('users:login')
    url = reverse(url_name, args=(comment.pk,))
    response = client.get(url)
    expected_url = f'{login_url}?next={url}'
    assertRedirects(response, expected_url)
