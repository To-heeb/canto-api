import os
import random
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(password: str):
    return pwd_context.hash(password)


def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def image_name(business_name, filename, filetype=None):
    # Make all characters lowercase and  Replace spaces with underscores
    business_name = business_name.lower().replace(" ", "_")

    # Extract the file extension
    file_extension = os.path.splitext(filename)[1]

    random_number = random.randint(9999, 100000000)

    if filetype is None:
        new_image_name = business_name+"_"+str(random_number)+file_extension
    else:
        new_image_name = business_name+"_"+"display_image"+file_extension

    return new_image_name


def image_directory():
    # Get the current directory
    current_directory = os.getcwd()
    # Move two steps back
    new_image_directory = os.path.abspath(os.path.join(current_directory, ".."))
    #print(new_image_directory)
    new_image_directory = os.path.join(new_image_directory, "")

    return new_image_directory


def image_url(image_name):
    #print(new_image_directory)
    image_path = "images/"+image_name

    return image_path