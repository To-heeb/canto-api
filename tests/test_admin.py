import pytest
from jose import jwt
from app import schemas

from app.config import settings


def test_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "message":  "Welcome to canto api, https://canto-api.onrender.com/docs"
    }


def test_create_admin(client):
    res = client.post("/admins/", json={
        "first_name": "Habib",
        "last_name": "Oyekola",
        "email": "habib@gmail.com",
        "password": "password",
        "role": "regular_admin"
    })

    admin = schemas.AdminOut(**res.json())
    assert admin.email == "habib@gmail.com"
    assert res.status_code == 201


def test_admin_login(client, test_user):
    res = client.post(
        "/admins/login",
        data={
            "username": test_user['email'],
            "password": test_user['password']
        })
    login_response = schemas.Token(**res.json())
    payload = jwt.decode(login_response.access_token,
                         settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get("admin_id")
    assert id == test_user['id']
    assert login_response.token_type == "bearer"
    assert res.status_code == 200


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


def test_get_all_admins(authorized_client):
    res = authorized_client.get("/admins/")

    def validate(business_map):
        return schemas.AdminOut(**business_map)
    admin_map = map(validate, res.json())
    admin_list = list(admin_map)

    assert res.status_code == 200


def test_unauthorized_user_get_all_admins(client):
    res = client.get("/admins/")

    assert res.status_code == 401


def test_regular_admin_cannot_get_all_admins(authorized_client2):
    res = authorized_client2.get(f"/admins/")

    assert res.status_code == 403


def test_get_one_admin(authorized_client, test_user):
    res = authorized_client.get(f"/admins/{test_user['id']}")
    admin = schemas.AdminOut(**res.json())

    assert res.status_code == 200
    assert admin.email == test_user['email']
    assert admin.first_name == test_user['first_name']
    assert admin.role == test_user['role']


def test_unauthorized_user_get_one_admin(client, test_user):
    res = client.get(f"/admins/{test_user['id']}")

    assert res.status_code == 401


def test_regular_admin_cannot_get_another_admin(authorized_client2, test_user):
    res = authorized_client2.get(f"/admins/{test_user['id']}")

    assert res.status_code == 403


def test_get_one_business_type_that_does_not_exist(authorized_client):
    res = authorized_client.get(f"/admins/88888")
    assert res.status_code == 404


def test_update_admin(authorized_client, test_user):
    data = {
        "first_name": "Haarith",
        "last_name": "Oyekola",
        "email": "haarith@gmail.com",
        "password": "password",
        "role": "super_admin"
    }

    res = authorized_client.put(
        f"/admins/{test_user['id']}", json=data)
    updated_admin = schemas.AdminOut(**res.json())
    assert res.status_code == 200
    assert updated_admin.first_name == data["first_name"]
    assert updated_admin.email == data["email"]
    assert updated_admin.role == data["role"]


def test_unauthorized_user_update_admin(client, test_user):

    data = {
        "first_name": "Haarith",
        "last_name": "Oyekola",
        "email": "haarith@gmail.com",
        "password": "password",
        "role": "super_admin"
    }

    res = client.put(
        f"/admins/{test_user['id']}", json=data)
    assert res.status_code == 401


def test_super_admin_can_update_other_admins(authorized_client, test_user2):
    data = {
        "first_name": "Haarith",
        "last_name": "Oyekola",
        "email": "haarith@gmail.com",
        "password": "password",
        "role": "super_admin"
    }

    res = authorized_client.put(
        f"/admins/{test_user2['id']}", json=data)
    updated_admin = schemas.AdminOut(**res.json())
    assert res.status_code == 200
    assert updated_admin.first_name == data["first_name"]
    assert updated_admin.email == data["email"]
    assert updated_admin.role == data["role"]


def test_regular_admin_can_not_update_other_admins(authorized_client2, test_user, test_user2):
    data = {
        "first_name": "Haarith",
        "last_name": "Oyekola",
        "email": "haarith@gmail.com",
        "password": "password",
        "role": "super_admin"
    }

    res = authorized_client2.put(
        f"/admins/{test_user['id']}", json=data)
    assert res.status_code == 403


def test_regular_admin_can_not_update_thier_role_to_super_admin(authorized_client2, test_user, test_user2):
    data = {
        "first_name": "Haarith",
        "last_name": "Oyekola",
        "email": "haarith@gmail.com",
        "password": "password",
        "role": "super_admin"
    }

    res = authorized_client2.put(
        f"/admins/{test_user2['id']}", json=data)
    updated_admin = schemas.AdminOut(**res.json())
    assert updated_admin.role != data["role"]
    assert updated_admin.role == "regular_admin"


def test_delete_admin(authorized_client, test_user):
    res = authorized_client.delete(
        f"/admins/{test_user['id']}")

    assert res.status_code == 204


def test_unauthorized_user_delete_admin(client, test_user):
    res = client.delete(
        f"/admins/{test_user['id']}")
    assert res.status_code == 401


def test_super_admin_can_delete_other_admins(authorized_client, test_user2):
    res = authorized_client.delete(
        f"/admins/{test_user2['id']}")

    assert res.status_code == 204


def test_regular_admin_can_not_delete_other_admins(authorized_client2, test_user):
    res = authorized_client2.delete(
        f"/admins/{test_user['id']}")
    assert res.status_code == 403
