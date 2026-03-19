import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..app import main, oauth2, schema, models
from ..app import main, models
from ..app.database import get_db
from ..app.oauth2 import create_access_token
from ..app.schema import Token
from ..app.models import Post
from ..app.config import settings

app = main.app

TEST_DATABASE_URL = f'postgresql://{settings.db_username}:{settings.db_password}@{settings.db_host}:{settings.db_port}/{settings.db_name}'
test_engine = create_engine(TEST_DATABASE_URL)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

@pytest.fixture()
def session():
    models.Base.metadata.drop_all(bind=test_engine)
    models.Base.metadata.create_all(bind=test_engine)
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(session):
    def override_get_db():
        yield session
    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)


@pytest.fixture
def test_user(client):
    user_data = {"name": "John",
                 "email": "user@example.com",
                 "password": "pass"}
    res = client.post('/users/', json=user_data)

    new_user = res.json()
    new_user["password"] = user_data['password']
    return new_user


@pytest.fixture
def token(client, test_user):
    return create_access_token({"user_id": test_user['id']})
    # res = client.post('/login', data={"username": test_user['email'], "password": test_user['password']})
    # token = Token(**res.json())
    # return token.access_token


@pytest.fixture
def authorize_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f'Bearer {token}'  # essential space after Bearer / пробел обязательно поcле Bearer
    }
    return client


# client.headers — это способ задать «какие заголовки всегда будут отправляться»,
# а `"Authorization"` — ключевой заголовок для передачи токена доступа

# - client в твоём тесте — это объект TestClient из Starlette/FastAPI.
# - У него есть атрибут .headers, который представляет собой словарь HTTP‑заголовков, отправляемых при каждом запросе.
# - Когда ты пишешь:
# client.headers = {
#     **client.headers,
#     "Authorization": f"Bearer {token}"}
# - ты добавляешь заголовок Authorization ко всем последующим запросам, чтобы они проходили аутентификацию.


posts = [{"title": "The first title", "content": "This is the first title", "published": True, "user_id": 1},
         {"title": "Second title", "content": "I love python", "published": True, "user_id": 1},
         {"title": "The tree titles", "content": "I wana be a doctor", "published": True, "user_id": 1}]


def create_model_post(post: dict):
    post = Post(**post)
    return post


@pytest.fixture
def test_posts(authorize_client, session):
    post_map = map(create_model_post, posts)
    # res = authorize_client.post('/posts/', json=post)
    session.add_all(list(post_map))
    session.commit()
    posts_query = session.query(Post).all()
    return posts_query
