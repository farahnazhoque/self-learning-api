from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") # what kind of hashing algorithm we will be using

def hash_password(password):
    return pwd_context.hash(password)

def verify(actual_password, hashed_password):
    return pwd_context.verify(actual_password, hashed_password)