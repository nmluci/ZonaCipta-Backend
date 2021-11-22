from datetime import datetime
from flask_restx import Namespace, Resource
from flask import request, make_response, jsonify
import pytz

from app.baseModel import FailedResponse, SuccessResponse
from app.reservation.models import BookedItem, PayData, UserBooks
from app.reservation.services import bookNewRoom, getUserBooking, verifyPayment

"""
ROUTING

base uri: /api/book

POST / - Register a new order
GET  /<string:uname> - GET all order for specified uname
POST /<string:uname>/pay - Submit payment related stuff for verification (e.g. using Payment Gateaway)
"""

reservation_np = Namespace("book")

@reservation_np.route("/")
class Books(Resource):
    def post(self):
        """
        Request:
        {
            "username" - customer's username
            "product_id" - room's item id
            "reserved_time" - reserved time
            "sum" - total
        }

        Return
        {
            "status": "OK",
            data: [
                {
                    "order_id" - order id
                    "username" - customer's username
                    "product_id" - room's item id
                    "product_name" - packag's name
                    "reserved_time" - reserved time
                    "date_created" - date created
                    "done" - stats
                    "price" - price
                    "total_price" - total to pay
                }
            ]
        }
        """
        try:
            req = request.get_json()
            if not req:
                raise Exception("Invalid JSON Body")

            newBook = BookedItem(
                username=req.get("username"),
                productId=req.get("product_id"),
                reserveTime=datetime.strptime(req.get("reserved_time"), 
                                "%Y-%m-%d %H:%M:%S"),
                sum=req.get("sum")
            )

            bookNewRoom(newBook)
            return make_response(SuccessResponse(
                data=[newBook.toJson()]
            ).toJson(), 200)
        except Exception as e:
            print(e)
            return make_response(FailedResponse(
                errorMessage=str(e)
            ).toJson(), 400)
            
@reservation_np.route("/<string:uname>")
class BookDetail(Resource):
    def get(self, uname):
        """
        Request 
        None

        Return
        {
            "status": "OK",
            data: [
                {
                    "username" - username
                    "order_id" - order_id
                    "sum" - sum
                    "grand_total" - sum of all items combined
                    "done" - paid boolean
                    "items": [
                        {
                            "product_id" - item id
                            "product_name" - package's name
                            "reserved_time" - reserved time
                            "price" - price
                            "sum" - sum
                            "total_price" - total to pay
                        }
                                        .
                                        .
                                        .
                    ]
                }
            ]
        }
        """
        try:
            userBooking = UserBooks(
                username=uname
            )

            getUserBooking(userBooking)

            return make_response(SuccessResponse(
                data=[userBooking.toJson()]
            ).toJson(), 200)
        except Exception as e:
            import traceback
            traceback.print_exc()
            return make_response(FailedResponse(
                errorMessage=str(e)
            ).toJson(), 400)

@reservation_np.route("/<string:uname>/pay")
class Book(Resource):
    def post(self, uname):
        """
        Request
        {
            "username" - username
            "first_name" - user's first name
            "last_name" - user's last name
            "order_id" - order's id
            "sign_key" - cryptographically secure hashed key
            "total_price" - total price
        }

        Return
        {
            "status": "OK"
        }
        """
        
        try:
            req = request.get_json()
            if not req:
                raise Exception("Invalid JSON Body")

            verifyData = PayData(
                username=req.get("username"),
                firstName=req.get("first_name"),
                lastName=req.get("last_name"),
                orderid=req.get("order_id"),
                signKey=req.get("sign_key"),
                totalPrice=req.get("total_price")
            )
            
            if not verifyPayment(verifyData):
                raise Exception("Invalid Sign Key")
            
            return make_response(SuccessResponse().toJson(), 200)
        except Exception as e:
            print(e)
            return make_response(FailedResponse(
                errorMessage=str(e)
            ).toJson(), 400)

