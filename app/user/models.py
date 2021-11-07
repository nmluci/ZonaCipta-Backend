from __future__ import annotations

from dataclasses import dataclass
from app.baseModel import db

class Users(db.Model):
    __tablename__ = "Users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, unique=True, nullable=False)
    email = db.Column(db.Text, unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    salt = db.Column(db.Text, nullable=False)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)

    def insert(self):
        db.session.add(self)
        db.session.commit()
        return self.id
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

@dataclass
class UserData:
    username: str
    password: str
    email: str = None
    firstName: str = None
    lastName: str = None
    id: int = None

    def toJson(cls, debug=False):
        res = {
            "username": cls.username,
            "email": cls.email,
        }

        if cls.firstName:
            res["first_name"] = cls.firstName
        if cls.lastName:
            res["last_name"] = cls.lastName
        if debug: 
            res["password"] = cls.password
        if cls.id: 
            res["id"] = cls.id
        return res