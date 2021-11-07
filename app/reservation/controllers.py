from flask_restx import Namespace, Resource
from flask import request, make_response, jsonify

"""
ROUTING

base uri: /api/book

GET / - Get ALL Hotels (Required DEV-TOKEN)
POST / - Register a new order based on a given data

GET /<int:uid> - GET all order for specified uid
POST /<int:uid> - Submit new order for specified uid 
"""

reservation_np = Namespace("book")

@reservation_np.route("/")
class Books(Resource):
    def post(self):
        """
        Request:
        {
            "uuid" - Device's uuid
            "customer_name" - Customer's name
            "customer_email" - Customer's email
            "customer_phone" - Customer's phone
        }

        Return
        {
            data: [
                "id" - id
                "customer_name" - Customer's name
                "customer_email" - Customer's email
                "customer_phone" - Customer's phone
                "date_created" - date created
                "done" 
            ]
        }
        """

@reservation_np.route("/<int:uid>")
class Book(Resource):
    pass

