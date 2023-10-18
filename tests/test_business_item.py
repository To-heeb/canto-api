import pytest
from app import schemas


def test_get_all_business_items(authorized_client, test_business_items):
    res = authorized_client.get("/business/item/")

    def validate(business_item):
        return schemas.BusinessItemOut(**business_item)
    business_item_map = map(validate, res.json())
    business_list = list(business_item_map)

    assert len(res.json()) == len(test_business_items)
    assert res.status_code == 200


def test_unauthorized_user_get_all_busineess_items(client):
    res = client.get("/business/item/")
    assert res.status_code == 401


def test_get_all_items_for_a_business(authorized_client, test_business_items, test_businesses):
    res = authorized_client.get(f"/business/{test_businesses[0].id}/item/")

    def validate(business_item):
        return schemas.BusinessItemOut(**business_item)
    business_item_map = map(validate, res.json())
    business_list = list(business_item_map)

    def filter_business(business_item):
        return business_item.status == 1 and business_item.business_id == test_businesses[0].id

    business_filter = filter(filter_business, test_business_items)

    assert len(res.json()) == len(list(business_filter))
    assert res.status_code == 200


def test_unauthorized_user_get_all_items_for_a_business(client, test_businesses):
    res = client.get(f"/business/{test_businesses[0].id}/item/")
    assert res.status_code == 401


def test_get_one_busineess_item(authorized_client, test_business_items):
    res = authorized_client.get(f"/business/item/{test_business_items[0].id}")
    business_item = schemas.BusinessItemOut(**res.json())
    assert business_item.id == test_business_items[0].id
    assert business_item.name == test_business_items[0].name
    assert business_item.status == test_business_items[0].status


def test_unauthorized_user_get_one_busineess_item(client, test_business_items):
    res = client.get(f"/business/item/{test_business_items[0].id}")
    assert res.status_code == 401


def test_get_one_busineess_item_that_does_not_exist(authorized_client):
    res = authorized_client.get(f"/business/item/88888")
    assert res.status_code == 404


@pytest.mark.parametrize("name, status, business_id", [
    ("Puff puff", 0, 2),
    ("Semo", 1, 2)
])
def test_create_business_item(authorized_client, test_businesses, name, status, business_id):
    res = authorized_client.post(
        "/business/item/", json={"name": name, "status": status, "business_id": business_id})

    business_item = schemas.BusinessItemOut(**res.json())
    assert res.status_code == 201
    assert business_item.name == name
    assert business_item.status == status
    assert business_item.business_id == business_id


def test_unauthorized_user_create_business_item(client):
    res = client.post(
        "/business/item/", json={"name": 'name', "status": 1, "business_id": 1})
    assert res.status_code == 401


def test_create_business_items(authorized_client, test_businesses):
    data = {
        "items": [
            {
                "name": "Puff puff",
                "status": 0,
                "business_id": 1
            },
            {
                "name": "Bonse",
                "status": 1,
                "business_id": 2
            },
            {
                "name": "Bread",
                "status": 1,
                "business_id": 2
            }
        ]
    }
    res = authorized_client.post(
        "/business/items/", json=data)

    assert res.status_code == 201
    assert len(res.json()["items"]) == len(data["items"])


def test_unauthorized_user_create_business_items(client):
    data = {
        "items": [
            {
                "name": "Puff puff",
                "status": 0,
                "business_id": 1
            },
            {
                "name": "Bonse",
                "status": 1,
                "business_id": 2
            },
            {
                "name": "Bread",
                "status": 1,
                "business_id": 2
            }
        ]
    }

    res = client.post(
        "/business/items/", json=data)

    assert res.status_code == 401


def test_update_business_item(authorized_client, test_businesses, test_business_items):
    data = {
        "name": "updated name",
        "status": 1,
        "business_id": test_businesses[0].id

    }
    res = authorized_client.put(
        f"/business/item/{test_business_items[0].id}", json=data)
    updated_business_item = schemas.BusinessItemOut(**res.json())
    assert res.status_code == 200
    assert updated_business_item.name == data['name']
    assert updated_business_item.status == data['status']


def test_unauthorized_user_update_business_item(client, test_businesses, test_business_items):
    data = {
        "name": "updated name",
        "status": 1,
        "business_id": test_businesses[0].id
    }

    res = client.put(
        f"/business/item/{test_business_items[0].id}", json=data)
    assert res.status_code == 401


def test_update_business_item_that_does_not_exist(authorized_client, test_businesses, test_business_items):
    data = {
        "name": "updated name",
        "status": 1,
        "business_id": test_businesses[1].id

    }
    res = authorized_client.put(f"/business/item/999", json=data)
    print(res.json())
    assert res.status_code == 404


def test_delete_business_item(authorized_client, test_business_items):
    res = authorized_client.delete(
        f"/business/item/{test_business_items[0].id}")

    assert res.status_code == 204


def test_unauthorized_user_delete_business_item(client, test_business_items):
    res = client.delete(
        f"/business/item/{test_business_items[0].id}")
    assert res.status_code == 401


def test_delete_business_item_that_does_not_exist(authorized_client):
    res = authorized_client.delete(
        f"/business/item/99")

    assert res.status_code == 404
