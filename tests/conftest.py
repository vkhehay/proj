import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ..app import main, database, oauth2, schema, models

app = main.app
get_db = database.get_db
Base = database.Base
create_access_token = oauth2.create_access_token
Token = schema.Token
Post = models.Post


DATABASE_URL = "postgresql://postgres:1234@localhost:5432/fastapi_test"
engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture  # (scope = "function"/"module"/"session") --> fixture running frequency
def session():  # session.query(models.Post)...
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


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
