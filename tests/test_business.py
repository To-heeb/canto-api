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


def test_get_one_business(authorized_client, test_businesses):
    res = authorized_client.get(f"/business/{test_businesses[0].id}")
    business = schemas.BusinessOut(**res.json())

    assert res.status_code == 200
    assert business.id == test_businesses[0].id
    assert business.name == test_businesses[0].name
    assert business.description == test_businesses[0].description


@pytest.mark.parametrize("name, description, location, business_type_id", [
    ("Mama Akara Spot 4", "This is the sales of Akara and Akamu",  "Behind Block 54", 1),
    ("Mama Akara Spot 3", "This is the sales of Akara and Akamu",  "Behind Block 53", 1)
])
def test_create_business_type(authorized_client, name, description, location, business_type_id):
    res = authorized_client.post(
        "/business/",
        json={
            "name": name,
            "description": description,
            "location": location,
            "business_type_id": business_type_id
        })

    business = schemas.BusinessOut(**res.json())
    assert res.status_code == 201
    assert business.name == name
    assert business.description == description
    assert business.location == location


def test_unauthorized_user_create_business_type(client, test_business_types):
    res = client.post(
        "/business/",
        json={
            "name": "Mama Akara Spot 2",
            "location": "Behind Block 52",
            "business_type_id": test_business_types[0].id,
            "description": "This is the sales of Akara and Akamu",
            "opened_at": "19:00",
            "closed_at": "20:30"
        })
    assert res.status_code == 401
