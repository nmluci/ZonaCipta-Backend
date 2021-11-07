from hashlib import new
from logging import error
from flask_restx import Namespace, Resource
from flask import request, make_response
import json

from app.baseModel import FailedResponse, SuccessResponse, config
from app.user.models import UserData
from app.user.services import registerNewUser, verifyUser

"""
ROUTING

base uri: /api/users

POST / - Register a new users
POST /auth - authenticate a user
"""

user_np = Namespace("users")

@user_np.route("/")
class Users(Resource):
    def post(self):
        """
        Request:
        Header: ZC-DEV-KEY -- optional (for debugging)
        {
            "username" - proposed username
            "password" - proposed password
            "first_name" - user's first name
            "last_name" - user's last name
            "email" - user's email
        }

        Return
        {
            "status": "OK",
            data: [
                {
                    "id" - id
                    "username" - username
                    "password" - hashed password (debugging only)
                    "email" - user's email
                    "first_name" - user's first name
                    "last_name" - user's last name
                }
            ]
        }
        """
        try:
            hed = request.headers.get("ZC-DEV-KEY")
            isProd = False if (not hed) or (hed != config.get("DEV_KEY")) else True

            req = request.get_json()
            if not req:
                raise Exception("Invalid JSON Body")

            newUser = UserData(
                username=req.get("username"),
                password=req.get("password"),
                firstName=req.get("first_name"),
                lastName=req.get("last_name"),
                email=req.get("email")
            )
            registerNewUser(newUser)

            return make_response(SuccessResponse(
                data=[newUser.toJson()]
            ).toJson(), 300)

        except Exception as e:
            print(e)
            return make_response(FailedResponse(
                errorMessage=str(e),
            ).toJson(), 400)

@user_np.route("/auth")
class User(Resource):
    def post(self):
        """
        Request
        {
            "username" - username
            "password" - plaintext passworc
        }

        Return
        {
            "status": "OK",
            data: [
                "id" - id
                "username" - username
                "email" - email
                "first_name" - first name
                "last_name" - last name
            ]
        }
        """
        try:
            req = request.get_json()
            if not req:
                raise Exception("Invalid JSON Body")
            
            user = UserData(
                username=req.get("username"),
                password=req.get("password")
            )

            if not verifyUser(user):
                raise Exception("Invalid Credentials")
            
            return make_response(SuccessResponse(
                data=[user.toJson()]
            ).toJson(), 300)
        except Exception as e:
            print(e)
            return make_response(FailedResponse(
                errorMessage=str(e)
            ).toJson(), 400)