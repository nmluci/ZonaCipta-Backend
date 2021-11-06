from flask_restx import Namespace, Resource
from flask import request, make_response, jsonify

reservation_np = Namespace("book")

@reservation_np.route("/")
class Books(Resource):
    pass

@reservation_np.route("/<int:uid>")
class Book(Resource):
    pass

