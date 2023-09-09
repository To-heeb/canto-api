import os
import random
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(password: str):
    return pwd_context.hash(password)

def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def image_name(business_name, image_name):
    # Make all characters lowercase and  Replace spaces with underscores
    business_name = business_name.lower().replace(" ", "_")
    
    # Extract the file extension
    file_extension = os.path.splitext(image_name)[1]
    
    random_number = random.randint(9999, 100000000) 
    
    image_name = business_name+"_"+str(random_float)+file_extension

    return image_name