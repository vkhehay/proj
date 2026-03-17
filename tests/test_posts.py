import pytest
from ..app.schema import PostVote, PostResponse, PostCreate


def test_get_post(authorize_client, test_posts):
    response = authorize_client.get('/posts/')
    assert response.status_code == 200


def test_post_id(authorize_client, test_posts):
    res = authorize_client.get(f'/posts/{test_posts[0].id}')
    post = PostVote(**res.json())
    assert post.post.id == test_posts[0].id
    assert post.post.content == test_posts[0].content


@pytest.mark.parametrize("title, content, published", [
    ("My first title", "Awsome title", True),
    ("Second title", "I love python", True),
    ("The tree titles", "I wana be a doctor", True)])
def test_create_post(authorize_client, test_posts, test_user, title, content, published):
    res = authorize_client.post('/posts/', json={"title": title, "content": content,
                                                 "published": published})
    created_post = PostResponse(**res.json())

    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.owner.email == test_user["email"]


def test_delete_post(authorize_client, test_posts, test_user):
    post_id = test_posts[1].id
    url = f"/posts/{post_id}"
    res = authorize_client.delete(url)

    assert res.status_code == 204


def test_update_post(authorize_client, test_posts):
    data = {"title": "blabla", "content": "another blalba", "published": False}
    url = f"/posts/{test_posts[2].id}"
    res = authorize_client.put(url, json=data)

    assert res.status_code == 202
    updated_post = res.json()   # PostResponce(**res.json()) не правильный вывод данных и приводит к ошибке.
    assert updated_post["title"] == data["title"]
    assert updated_post["content"] == data["content"]
    assert updated_post["published"] == data["published"]
    assert "id" in updated_post
    assert "created_at" in updated_post
    assert "owner" in updated_post
