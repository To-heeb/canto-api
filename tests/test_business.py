import pytest
from app import schemas


def test_get_all_businesses(authorized_client, test_businesses):
    res = authorized_client.get("/business/")

    def validate(business_map):
        return schemas.BusinessOut(**business_map)
    business_map = map(validate, res.json())
    business_list = list(business_map)

    assert len(res.json()) == len(test_businesses)
    assert res.status_code == 200


def test_unauthorized_user_get_all_businesses(client, test_businesses):
    res = client.get("/business/")

    def validate(business_map):
        return schemas.BusinessOut(**business_map)
    business_map = map(validate, res.json())
    business_list = list(business_map)

    assert len(res.json()) == len(test_businesses)
    assert res.status_code == 200


def test_get_one_business(authorized_client, test_businesses):
    res = authorized_client.get(f"/business/{test_businesses[0].id}")
    business = schemas.BusinessOut(**res.json())

    assert res.status_code == 200
    assert business.id == test_businesses[0].id
    assert business.name == test_businesses[0].name
    assert business.description == test_businesses[0].description


def test_unauthorized_user_get_one_business(client, test_businesses):
    res = client.get(f"/business/{test_businesses[0].id}")
    business = schemas.BusinessOut(**res.json())

    assert res.status_code == 200
    assert business.id == test_businesses[0].id
    assert business.name == test_businesses[0].name
    assert business.description == test_businesses[0].description


def test_get_one_business_type_that_does_not_exist(authorized_client):
    res = authorized_client.get(f"/business/type/88888")
    assert res.status_code == 404


@pytest.mark.parametrize("name, description, location, business_type_id, status", [
    ("Mama Akara Spot 4", "This is the sales of Akara and Akamu",
     "Behind Block 54", 1, 1),
    ("Mama Akara Spot 3", "This is the sales of Akara and Akamu",
     "Behind Block 53", 1, 0)
])
def test_create_business_type(authorized_client, test_business_types, name, description, location, business_type_id, status):
    res = authorized_client.post(
        "/business/",
        json={
            "name": name,
            "description": description,
            "location": location,
            "business_type_id": business_type_id,
            "status": status,
            "working_hours": {
                "1": {"opened_at": "19:00:00", "closed_at": "20:20:00"},
                "2": {"opened_at": "19:00:00", "closed_at": "20:20:00"},
                "3": {"opened_at": "19:00:00", "closed_at": "20:20:00"},
                "4": {"opened_at": "19:00:00", "closed_at": "20:20:00"},
                "5": {"opened_at": "19:00:00", "closed_at": "20:20:00"},
                "6": {"opened_at": "19:00:00", "closed_at": "00:00:00"},
                "7": {"opened_at": "00:00:00", "closed_at": "00:00:00"}
            }
        })
    business = schemas.BusinessOut(**res.json())
    assert res.status_code == 201
    assert business.name == name
    assert business.description == description
    assert business.location == location
    assert business.status == status


def test_unauthorized_user_create_business(client, test_business_types, ):
    res = client.post(
        "/business/",
        json={
            "name": "Mama Akara Spot 2",
            "location": "Behind Block 52",
            "business_type_id": test_business_types[0].id,
            "description": "This is the sales of Akara and Akamu",
            "status": 1,
            "working_hours": {
                "1": {"opened_at": "19:00:00", "closed_at": "20:20:00"},
                "2": {"opened_at": "19:00:00", "closed_at": "20:20:00"},
                "3": {"opened_at": "19:00:00", "closed_at": "20:20:00"},
                "4": {"opened_at": "19:00:00", "closed_at": "20:20:00"},
                "5": {"opened_at": "19:00:00", "closed_at": "20:20:00"},
                "6": {"opened_at": "19:00:00", "closed_at": "00:00:00"},
                "7": {"opened_at": "00:00:00", "closed_at": "00:00:00"}
            }
        })
    assert res.status_code == 401


def test_delete_business(authorized_client, test_businesses):
    res = authorized_client.delete(
        f"/business/{test_businesses[0].id}")

    assert res.status_code == 204


def test_unauthorized_user_delete_business(client, test_businesses):
    res = client.delete(
        f"/business/{test_businesses[0].id}")
    assert res.status_code == 401


def test_delete_business_that_does_not_exist(authorized_client):
    res = authorized_client.delete(
        f"/business/99")

    assert res.status_code == 404


def test_update_business(authorized_client, test_business_types, test_businesses):
    data = {
        "name": "Mama Akara Spot 6",
        "location": "Behind Block 52",
        "business_type_id": test_business_types[0].id,
        "description": "This is the sales of Akara and Akamu",
        "status": 1,
        "working_hours": {
                "1": {"opened_at": "19:00:00", "closed_at": "20:20:00"},
                "2": {"opened_at": "19:00:00", "closed_at": "20:20:00"},
                "3": {"opened_at": "19:00:00", "closed_at": "20:20:00"},
                "4": {"opened_at": "19:00:00", "closed_at": "20:20:00"},
                "5": {"opened_at": "19:00:00", "closed_at": "20:20:00"},
                "6": {"opened_at": "19:00:00", "closed_at": "00:00:00"},
                "7": {"opened_at": "00:00:00", "closed_at": "00:00:00"}
        }
    }
    res = authorized_client.put(
        f"/business/{test_businesses[0].id}", json=data)
    updated_business = schemas.BusinessOut(**res.json())
    assert res.status_code == 200
    assert updated_business.name == data["name"]
    assert updated_business.description == data["description"]
    assert updated_business.location == data["location"]
    assert updated_business.status == data["status"]


def test_unauthorized_user_update_business(client, test_business_types, test_businesses):

    data = {
        "name": "Mama Akara Spot 2",
        "location": "Behind Block 52",
        "business_type_id": test_business_types[0].id,
        "description": "This is the sales of Akara and Akamu",
        "status": 1,
        "working_hours": {
            "1": {"opened_at": "19:00:00", "closed_at": "20:20:00"},
            "2": {"opened_at": "19:00:00", "closed_at": "20:20:00"},
            "3": {"opened_at": "19:00:00", "closed_at": "20:20:00"},
            "4": {"opened_at": "19:00:00", "closed_at": "20:20:00"},
            "5": {"opened_at": "19:00:00", "closed_at": "20:20:00"},
            "6": {"opened_at": "19:00:00", "closed_at": "00:00:00"},
            "7": {"opened_at": "00:00:00", "closed_at": "00:00:00"}
        }
    }
    res = client.put(
        f"/business/{test_businesses[0].id}", json=data)
    assert res.status_code == 401


def test_update_business_that_does_not_exist(authorized_client, test_business_types):
    data = {
        "name": "Mama Akara Spot 2",
        "location": "Behind Block 52",
        "business_type_id": test_business_types[0].id,
        "description": "This is the sales of Akara and Akamu",
        "status": 1,
        "working_hours": {
            "1": {"opened_at": "19:00:00", "closed_at": "20:20:00"},
            "2": {"opened_at": "19:00:00", "closed_at": "20:20:00"},
            "3": {"opened_at": "19:00:00", "closed_at": "20:20:00"},
            "4": {"opened_at": "19:00:00", "closed_at": "20:20:00"},
            "5": {"opened_at": "19:00:00", "closed_at": "20:20:00"},
            "6": {"opened_at": "19:00:00", "closed_at": "00:00:00"},
            "7": {"opened_at": "00:00:00", "closed_at": "00:00:00"}
        }
    }

    res = authorized_client.put(
        f"/business/99", json=data)

    assert res.status_code == 404


def test_search_business(authorized_client, test_businesses):
    res = authorized_client.get(
        f"/business/search?keyword=Akara")

    def validate(business_map):
        return schemas.BusinessOut(**business_map)
    business_map = map(validate, res.json())
    assert res.status_code == 200


def test_unauthorized_user_search_business(client, test_businesses):
    res = client.get(
        f"/business/search?keyword=Akara")

    def validate(business_map):
        return schemas.BusinessOut(**business_map)
    business_map = map(validate, res.json())
    assert res.status_code == 200


def test_search_business_that_does_not_exist(authorized_client, test_businesses):
    res = authorized_client.get(
        f"/business/search?keyword=erthegf")

    def validate(business_map):
        return schemas.BusinessOut(**business_map)
    business_map = map(validate, res.json())
    print(business_map)
    assert res.status_code == 200
