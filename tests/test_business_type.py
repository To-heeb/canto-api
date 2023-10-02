from app import schemas
from .database import session, client


def test_get_all_busineess_types(authorized_client, test_business_types):
    res = authorized_client.get("/business/type/")

    def validate(business_type):
        return schemas.BusinessTypeOut(**business_type)
    business_type_map = map(validate, res.json())
    business_type_list = list(business_type_map)

    assert len(res.json()) == len(test_business_types)
    assert res.status_code == 200
