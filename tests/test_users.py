import pytest
import jwt

from ..app.schema import UserResponse, Token
from ..app.models import User
from ..app.config import settings
# from .conftest import client, session '''if a conftest.py file is in test folder, no need to import pytest.fixtures'''


def test_create_user(client):
    res = client.post('/users/', json={"name": "John", "email": "email@i.ua", "password": "pass"})
    user = UserResponse(**res.json())
    assert user.email == "email@i.ua"
    assert res.status_code == 201


# @pytest.fixture
# def test_get_user(client, session): '''conftest.py @fixture.session must have arg (scope = 'module')'''
#     user_data = session.query(User).filter(User.name == "John").first()
#     new_user = user_data.__dict__
#     new_user["password"] = 'pass'
#     return new_user

#
# def test_root(client):
#     response = client.get('/')
#     assert response.json().get('message') == 'Hello'
#     assert response.status_code == 200


def test_login_user(client, test_user):
    res = client.post('/login', data={"username": test_user['email'], "password": test_user['password']})
    token = Token(**res.json()).access_token
    payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get("user_id")
    assert res.status_code == 200
    assert test_user["id"] == id
    # return id, token


@pytest.mark.parametrize("email, password, status_code", [
    ('wrong@email.com', "pass", 403),
    ('user@example.com', 'wrongPass', 403),
    (None, 'pass', 422),
    ('user@example.com', None, 422),
    ('user@example.com', 'pass', 200)
])
def test_wrong_login_user(client, test_user, email, password, status_code):
    res = client.post('/login', data={"username": email, "password": password})
    assert res.status_code == status_code


# def func(args):
#     raise Exception
#
#
# def test_insufficient_login(client, test_user):
#     with pytest.raises(Exception):  # to catch raised Exceptions and pass the tests
#         test_user.func(wrong_args='wrong args')



