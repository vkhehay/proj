import pytest
from ..app import models


@pytest.fixture
def test_vote(authorize_client, test_posts, session, test_user):
    new_vote = models.Vote(post_id=test_posts[0].id, user_id=test_user["id"])
    session.add(new_vote)
    session.commit()


def test_votes(authorize_client, test_posts):
    res = authorize_client.post('/vote/', json={"post_id": test_posts[0].id, "dir": 1})
    assert res.status_code == 201


def test_vote_twice(authorize_client, test_posts, test_vote):
    res = authorize_client.post('/vote/', json={"post_id": test_posts[0].id, "dir": 1})
    assert res.status_code == 409


def test_delete_vote(authorize_client, test_posts, test_vote):
    res = authorize_client.post('/vote/', json={"post_id": test_posts[0].id, "dir": 0})
    assert res.status_code == 201


def test_delete_vote_non_exist(authorize_client, test_posts, test_vote):
    res = authorize_client.post('/vote/', json={"post_id": test_posts[2].id, "dir": 0})
    assert res.status_code == 404