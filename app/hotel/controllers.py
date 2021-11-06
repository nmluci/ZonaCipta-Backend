from flask_restx import Namespace, Resource
from flask import request, make_response, jsonify

hotel_np = Namespace("hotels")

@hotel_np.route("/")
class Hotels(Resource):
    pass

@hotel_np.route("/<int:uid>")
class Cart(Resource):
    pass

