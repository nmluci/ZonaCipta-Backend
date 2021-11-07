from __future__ import annotations

from app.user.models import Users
from app.user.models import UserData
from app.baseModel import db

from typing import Tuple
import hashlib, hmac, os

def registerNewUser(metadata: UserData):
    if len(db.session.query(Users).filter(Users.username == metadata.username).all()):
        raise Exception("username already used")

    if len(db.session.query(Users).filter(Users.email == metadata.email).all()):
        raise Exception("email already registered")

    hashedPw, saltPw = passwordCooking(metadata.password)
    newUser = Users(
        username=metadata.username,
        email=metadata.email,
        password=hashedPw.hex(),
        salt=saltPw.hex(),
        first_name=metadata.firstName,
        last_name=metadata.lastName
    )

    id = newUser.insert()
    metadata.id = id
    metadata.password = hashedPw.hex()

def verifyUser(metadata: UserData) -> bool:
    userCred = db.session.query(Users).filter(Users.username == metadata.username).first()
    if not userCred:
        raise Exception("username isn't existed")

    metadata.email = userCred.email
    metadata.firstName = userCred.first_name
    metadata.lastName = userCred.last_name
    return passwordVerify(metadata.password, bytes.fromhex(userCred.password), bytes.fromhex(userCred.salt))
    
def passwordCooking(text: str) -> Tuple[bytes, bytes]:
    salt = os.urandom(16)
    pw_hash = hashlib.pbkdf2_hmac("sha256", text.encode(), salt, 100000)
    return (pw_hash, salt)

def passwordVerify(text: str, hashed: bytes, salt: bytes) -> bool:
    return hmac.compare_digest(
        hashed,
        hashlib.pbkdf2_hmac("sha256", text.encode(), salt, 100000)
    )