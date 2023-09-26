import os
import random
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    """_summary_

    Args:
        password (str): _description_

    Returns:
        _type_: _description_
    """
    return pwd_context.hash(password)


def verify(plain_password, hashed_password):
    """_summary_

    Args:
        plain_password (_type_): _description_
        hashed_password (bool): _description_

    Returns:
        _type_: _description_
    """
    return pwd_context.verify(plain_password, hashed_password)


def image_name(prefix_name, filename, filetype=None):
    """_summary_

    Args:
        prefix_name (_type_): _description_
        filename (_type_): _description_
        filetype (_type_, optional): _description_. Defaults to None.

    Returns:
        _type_: _description_
    """
    # Make all characters lowercase and  Replace spaces with underscores
    prefix_name = prefix_name.lower().replace(" ", "_")

    # Extract the file extension
    file_extension = os.path.splitext(filename)[1]

    random_number = random.randint(9999, 100000000)

    if filetype is None:
        new_image_name = prefix_name+"_"+str(random_number)+file_extension
    else:
        new_image_name = prefix_name+"_"+"display_image"+file_extension

    return new_image_name


def image_directory():
    """_summary_

    Returns:
        _type_: _description_
    """
    # Get the current directory
    current_directory = os.getcwd()
    # Move two steps back
    new_image_directory = os.path.abspath(
        os.path.join(current_directory, ".."))
    # print(new_image_directory)
    new_image_directory = os.path.join(new_image_directory, "")

    return new_image_directory


def image_url(image_name):
    """_summary_

    Args:
        image_name (_type_): _description_

    Returns:
        _type_: _description_
    """
    # print(new_image_directory)
    image_path = "images/"+image_name

    return image_path
