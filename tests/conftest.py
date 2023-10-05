from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app

from app.config import settings
from app.database import conn, Base
from app.oauth2 import create_access_token
from app import models


SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'


engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):
    def override_conn():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[conn] = override_conn
    yield TestClient(app)


@pytest.fixture
def test_user(client):
    user_data = {
        "first_name": "Toheeb",
        "last_name": "Oyekola",
        "email": "toheeb.olawale.to23@gmail.com",
        "password": "password",
        "role": "super_admin"
    }
    res = client.post('/admins', json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture
def token(test_user):
    return create_access_token({"admin_id":  test_user['id'], "admin_role": test_user['role']})


@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }

    return client


@pytest.fixture
def test_business_types(session):
    business_types_data = [
        {
            "name": "Street food",
            "description": "These are food sold on the street."
        },
        {
            "name": "Provisions",
            "description": "These are provision items.."
        },
        {
            "name": "Groceries",
            "description": "These are grocery items."
        }]

    def create_business_type_model(business_type):
        return models.BusinessType(**business_type)

    business_types_map = map(create_business_type_model, business_types_data)
    business_types_list = list(business_types_map)

    session.add_all(business_types_list)
    session.commit()

    business_types = session.query(models.BusinessType).all()
    return business_types


@pytest.fixture
def test_businesses(session, test_business_types):

    business_data = [
        {
            "name": "Mama Akara Spot 2",
            "location": "Behind Block 52",
            "business_type_id": test_business_types[0].id,
            "description": "This is the sales of Akara and Akamu",
            "opened_at": "19:00",
            "closed_at": "20:30"
        },
        {
            "name": "Mama Akara Spot 1",
            "location": "Behind Soldiers Club",
            "business_type_id": test_business_types[0].id,
            "description": "This is the sales of Akara and Akamu",
            "opened_at": "19:00",
            "closed_at": "20:30"
        }
    ]

    def create_business_model(business):
        return models.Business(**business)

    business_map = map(create_business_model, business_data)
    business_list = list(business_map)

    session.add_all(business_list)
    session.commit()

    businesses = session.query(models.Business).all()

    business_working_hours_data = [
        {
            "working_hours": {

                "1": {
                    "opened_at": "19:00:00",
                    "closed_at": "20:20:00"
                },
                "2": {
                    "opened_at": "19:00:00",
                    "closed_at": "20:20:00"
                },
                "3": {
                    "opened_at": "19:00:00",
                    "closed_at": "20:20:00"
                },
                "4": {
                    "opened_at": "19:00:00",
                    "closed_at": "20:20:00"
                },
                "5": {
                    "opened_at": "19:00:00",
                    "closed_at": "20:20:00"
                },
                "6": {
                    "opened_at": "19:00:00",
                    "closed_at": "00:00:00"
                },
                "7": {
                    "opened_at": "00:00:00",
                    "closed_at": "00:00:00"
                }
            }
        },
        {
            "working_hours": {
                "1": {
                    "opened_at": "19:00:00",
                    "closed_at": "20:20:00"
                },
                "2": {
                    "opened_at": "19:00:00",
                    "closed_at": "20:20:00"
                },
                "3": {
                    "opened_at": "19:00:00",
                    "closed_at": "20:20:00"
                },
                "4": {
                    "opened_at": "19:00:00",
                    "closed_at": "20:20:00"
                },
                "5": {
                    "opened_at": "19:00:00",
                    "closed_at": "20:20:00"
                },
                "6": {
                    "opened_at": "19:00:00",
                    "closed_at": "00:00:00"
                },
                "7": {
                    "opened_at": "00:00:00",
                    "closed_at": "00:00:00"
                }
            }
        }
    ]

    i = 0
    for business_working_time in business_working_hours_data:
        business_working_hours = business_working_time["working_hours"]
        for working_day, working_time in business_working_hours.items():
            new_working_hour = models.BusinessWorkingHours(
                business_id=businesses[i].id,
                weekday=working_day,
                opened_at=working_time["opened_at"],
                closed_at=working_time["closed_at"]
            )
            session.add(new_working_hour)
        i = i+1
        session.commit()
    # print(businesses[0].__dict__)
    return businesses
