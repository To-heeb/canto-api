# import os


# def test_add_business_images(authorized_client, test_businesses):
#     image1 = "pizza-cat.png"
#     image2 = "pizza-dog.png"
#     image3 = "pizza-fish.png"

#     # Check the current working directory and construct the image paths
#     current_directory = os.getcwd()
#     image1_path = os.path.abspath(
#         (os.path.join(current_directory, "tests", image1)))
#     image2_path = os.path.join(current_directory,  "tests", image2)
#     image3_path = os.path.join(current_directory,  "tests", image3)
#     image1_byte = open(image1_path, 'rb')
#     # print(image1_path)
#     # print(os.path.basename(image1_path))
#     files = {
#         "files": [
#             (image1, open(image1_path, 'rb')),
#             (image2, open(image2_path, 'rb')),
#             (image3, open(image3_path, 'rb'))
#         ],
#         "business_id": test_businesses[0].id
#     }

#     data = {
#         "business_id": test_businesses[0].id
#     }
#     headers = {
#         **authorized_client.headers,
#         "Content-Type": "multipart/form-data; boundary=1000000"
#     }
#     res = authorized_client.post(
#         "/business/image/", headers=headers, data=data, files=files)
#     # print(res.text)
#     print(res.json())
#     assert res.status_code == 201
#     assert res.message == "File(s) has been successfully uploaded."
