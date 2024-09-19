from passlib.context import CryptContext

cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")


def bcrypt(payload):
    return cxt.hash(payload)


def hash_verify(plain, hashed):
    return cxt.verify(plain, hashed)
