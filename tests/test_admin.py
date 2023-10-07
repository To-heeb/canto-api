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
        f"/admin/{test_user['id']}", json=data)
    print(res.json())
    updated_admin = schemas.AdminOut(**res.json())
    assert res.status_code == 200
    assert updated_admin.first_name == data["first_name"]
    assert updated_admin.email == data["email"]
    assert updated_admin.role == data["role"]


# def test_unauthorized_user_update_business(client, test_business_types, test_businesses):

#     data = {
#         "name": "Mama Akara Spot 2",
#         "location": "Behind Block 52",
#         "business_type_id": test_business_types[0].id,
#         "description": "This is the sales of Akara and Akamu",
#         "status": 1,
#         "working_hours": {
#             "1": {"opened_at": "19:00:00", "closed_at": "20:20:00"},
#             "2": {"opened_at": "19:00:00", "closed_at": "20:20:00"},
#             "3": {"opened_at": "19:00:00", "closed_at": "20:20:00"},
#             "4": {"opened_at": "19:00:00", "closed_at": "20:20:00"},
#             "5": {"opened_at": "19:00:00", "closed_at": "20:20:00"},
#             "6": {"opened_at": "19:00:00", "closed_at": "00:00:00"},
#             "7": {"opened_at": "00:00:00", "closed_at": "00:00:00"}
#         }
#     }
#     res = client.put(
#         f"/business/{test_businesses[0].id}", json=data)
#     assert res.status_code == 401


# def test_update_business_that_does_not_exist(authorized_client, test_business_types):
#     data = {
#         "name": "Mama Akara Spot 2",
#         "location": "Behind Block 52",
#         "business_type_id": test_business_types[0].id,
#         "description": "This is the sales of Akara and Akamu",
#         "status": 1,
#         "working_hours": {
#             "1": {"opened_at": "19:00:00", "closed_at": "20:20:00"},
#             "2": {"opened_at": "19:00:00", "closed_at": "20:20:00"},
#             "3": {"opened_at": "19:00:00", "closed_at": "20:20:00"},
#             "4": {"opened_at": "19:00:00", "closed_at": "20:20:00"},
#             "5": {"opened_at": "19:00:00", "closed_at": "20:20:00"},
#             "6": {"opened_at": "19:00:00", "closed_at": "00:00:00"},
#             "7": {"opened_at": "00:00:00", "closed_at": "00:00:00"}
#         }
#     }

#     res = authorized_client.put(
#         f"/business/99", json=data)

#     assert res.status_code == 404
