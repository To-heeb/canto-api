import pytest
from jose import jwt
from app import schemas
from .database import session, client

from app.config import settings


def test_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to canto api"}


def test_create_admin(client):
    response = client.post("/admins/", json={
        "first_name": "Habib",
        "last_name": "Oyekola",
        "email": "habib@gmail.com",
        "password": "password",
        "role": "regular_admin"
    })

    admin = schemas.AdminOut(**response.json())
    assert admin.email == "habib@gmail.com"
    assert response.status_code == 201


def test_admin_login(client, test_user):
    response = client.post(
        "/admins/login",
        data={
            "username": test_user['email'],
            "password": test_user['password']
        })
    login_response = schemas.Token(**response.json())
    payload = jwt.decode(login_response.access_token,
                         settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get("admin_id")
    assert id == test_user['id']
    assert login_response.token_type == "bearer"
    assert response.status_code == 200


@pytest.mark.parametrize("email, password, status_code", [
    ('mishmash@gmail.com', 'password123', 403),
    ('wronggmail.com', 'fishy', 403),
    ('bestbuy@gmail.com', 'hackme', 403),
    (None, 'password123', 422),
    ('yuppy@gmail.com', None, 422)
])
def test_incorrect_login(client, email, password, status_code):
    res = client.post(
        "/admins/login", data={"username": email, "password": password})

    assert res.status_code == status_code
