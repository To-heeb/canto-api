import pytest
from app import schemas


def test_get_all_busineess_types(authorized_client, test_business_types):
    res = authorized_client.get("/business/type/")

    def validate(business_type):
        return schemas.BusinessTypeOut(**business_type)
    business_type_map = map(validate, res.json())
    business_type_list = list(business_type_map)

    assert len(res.json()) == len(test_business_types)
    assert res.status_code == 200


def test_unauthorized_user_get_all_busineess_types(client):
    res = client.get("/business/type/")
    assert res.status_code == 401


def test_get_one_busineess_type(authorized_client, test_business_types):
    res = authorized_client.get(f"/business/type/{test_business_types[0].id}")
    business_type = schemas.BusinessTypeOut(**res.json())
    assert business_type.id == test_business_types[0].id
    assert business_type.name == test_business_types[0].name
    assert business_type.description == test_business_types[0].description


def test_unauthorized_user_get_one_busineess_type(client, test_business_types):
    res = client.get(f"/business/type/{test_business_types[0].id}")
    assert res.status_code == 401


def test_get_one_busineess_type_that_does_not_exist(authorized_client):
    res = authorized_client.get(f"/business/type/88888")
    assert res.status_code == 404


@pytest.mark.parametrize("name, description", [
    ("Street food", "awesome new content"),
    ("favorite pizza", "i love pepperoni")
])
def test_create_business_type(authorized_client, name, description):
    res = authorized_client.post(
        "/business/type/", json={"name": name, "description": description})

    business_type = schemas.BusinessTypeOut(**res.json())
    assert res.status_code == 201
    assert business_type.name == name
    assert business_type.description == description


def test_unauthorized_user_create_business_type(client):
    res = client.post(
        "/business/type/", json={"name": "arbitrary title", "description": "aasdfjasdf"})
    assert res.status_code == 401


def test_delete_business_type(authorized_client, test_business_types):
    res = authorized_client.delete(
        f"/business/type/{test_business_types[0].id}")

    assert res.status_code == 204


def test_unauthorized_user_delete_business_type(client, test_business_types):
    res = client.delete(
        f"/business/type/{test_business_types[0].id}")
    assert res.status_code == 401


def test_delete_business_type_that_does_not_exist(authorized_client):
    res = authorized_client.delete(
        f"/business/type/99")

    assert res.status_code == 404


def test_update_business_type(authorized_client, test_business_types):
    data = {
        "name": "updated name",
        "description": "updatd description",
        "id": test_business_types[0].id

    }
    res = authorized_client.put(
        f"/business/type/{test_business_types[0].id}", json=data)
    updated_business_types = schemas.BusinessTypeOut(**res.json())
    assert res.status_code == 200
    assert updated_business_types.name == data['name']
    assert updated_business_types.description == data['description']


def test_unauthorized_user_update_business_type(client, test_business_types):
    data = {
        "name": "updated name",
        "description": "updatd description",
        "id": test_business_types[0].id

    }

    res = client.put(
        f"/business/type/{test_business_types[0].id}", json=data)
    assert res.status_code == 401


def test_update_business_type_that_does_not_exist(authorized_client, test_business_types):
    data = {
        "name": "updated name",
        "description": "updatd description",
        "id": test_business_types[1].id

    }
    print(len(test_business_types))
    res = authorized_client.put(
        f"/business/type/99", json=data)

    assert res.status_code == 404
