

def test_add_business_images(authorized_client, test_businesses):
    image1 = "pizza-cat.jpg"
    image2 = "pizza-dog.png"
    image3 = "pizza-fish.gif"
    data = {
        'files': {
            (open(image1, 'rb'), image1),
            (open(image2, 'rb'), image2),
            (open(image3, 'rb'), image3)
        },
        "business_id": test_businesses[0].id
    }

    res = authorized_client.post(
        f"/business/image/", data=data)
    assert res.status_code == 201
    assert res.message == "File(s) has been successfully uploaded."
