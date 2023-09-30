from fastapi.testclient import TestClient
from app.main import app
from app import schemas
from .database import session, client


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to canto api"}


# def test_create_admin(client):
#     response = client.post("/admins/", json={
#         "first_name": "Habib",
#         "last_name": "Oyekola",
#         "email": "habib@gmail.com",
#         "password": "password",
#         "role": "regular_admin"
#     })

#     admin = schemas.AdminOut(**response.json())
#     assert response.status_code == 201
