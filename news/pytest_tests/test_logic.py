from http import HTTPStatus
import pytest
from pytest_django.asserts import assertRedirects, assertFormError

from django.urls import reverse

from news.forms import WARNING
from news.models import Comment


# Анонимный пользователь не может отправить комментарий.
@pytest.mark.django_db
def test_anonymous_user_cant_create_comment(
    client, news, comment_form_data
):
    url = reverse('news:detail', args=(news.pk,))
    login_url = reverse('users:login')
    response = client.post(url, data=comment_form_data)
    expected_url = f'{login_url}?next={url}'
    assertRedirects(response, expected_url)
    assert Comment.objects.count() == 0


# Авторизованный пользователь может отправить комментарий.
def test_authorized_user_can_create_comment(
        author_client, author, news, comment_form_data
):
    url = reverse('news:detail', args=(news.pk,))
    response = author_client.post(url, data=comment_form_data)
    assertRedirects(response, f'{url}#comments')
    assert Comment.objects.count() == 1
    new_comment = Comment.objects.get()

    assert new_comment.author == author
    assert new_comment.news == news
    assert new_comment.text == comment_form_data['text']


# # Если комментарий содержит запрещённые слова,
# # он не будет опубликован, а форма вернёт ошибку.
@pytest.mark.django_db
def test_user_cannot_use_swear_words(
    swear_word_data, news, author_client
):
    url = reverse('news:detail', args=(news.pk,))
    response = author_client.post(url, data=swear_word_data)
    expected_comment_count = 0
    assertFormError(response, form='form', field='text', errors=WARNING)
    assert Comment.objects.count() == expected_comment_count


# Авторизованный пользователь может редактировать свои комментарии
def test_author_can_edit_his_own_comment(
        author_client, news, comment, comment_form_data
):
    news_url = reverse('news:detail', args=(news.pk,))
    comment_url = reverse('news:edit', args=(comment.pk,))
    expected_url = f'{news_url}#comments'
    response = author_client.post(comment_url, data=comment_form_data)
    assertRedirects(response, expected_url)
    comment.refresh_from_db()
    assert comment.text == comment_form_data['text']
    assert Comment.objects.count() == 1


# Авторизованный пользователь может удалят свои комментарии
def test_author_can_delete_his_own_comment(
    author_client, news, comment
):
    news_url = reverse('news:detail', args=(news.pk,))
    comment_url = reverse('news:delete', args=(comment.pk,))
    expected_url = f'{news_url}#comments'
    response = author_client.post(comment_url)
    assertRedirects(response, expected_url)
    assert Comment.objects.count() == 0


# Авторизованный пользователь не может редактировать чужие комментарии
def test_other_user_cannot_edit_comment(
    not_author_client, comment, comment_form_data
):
    url = reverse('news:edit', args=(comment.pk,))
    response = not_author_client.post(url, data=comment_form_data)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment_from_db = Comment.objects.get()
    assert comment.author == comment_from_db.author
    assert comment.news == comment_from_db.news
    assert comment.text == comment_from_db.text


# Авторизованный пользователь не может удалять чужие комментарии
def test_other_user_cannot_delete_comment(
    not_author_client, comment
):
    url = reverse('news:delete', args=(comment.pk,))
    response = not_author_client.post(url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert Comment.objects.count() == 1
