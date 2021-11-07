from os import name
from flask_restx import Namespace, Resource
from flask import request, make_response, jsonify
import json

from app.baseModel import FailedResponse, SuccessResponse, config
from app.zone.models import DumpZoneData, ItemData, ZoneData
from app.zone.services import dumpAllHotel, registerNewItem, registerNewZone

"""
ROUTING

base uri: /api/hotels

GET / - Get ALL Hotels (Required DEV-TOKEN)
POST / - Register a new Hotel instance

GET /<int:uid> - GET all item sold by specified hotel
POST /<int:uid> - Submit new item for specified hotel 
"""

hotel_np = Namespace("zones")

@hotel_np.route("/")
class Zones(Resource):
    def get(self):
        """
        Request:
        Header: ZC-DEV-KEY

        Return
        {
            data: [
                {
                    "hotel_name" - hotel's name
                    "address" - hotel's address
                    "phone" - hotel's phone number
                    "id" - hotel id
                }
                                .
                                .
                                .
            ]
        }
        """
        try:
            hed = request.headers.get("ZC-DEV-KEY")
            if (not hed) or (hed != config.get("DEV_KEY")):
                raise Exception("WEAKLING!!!")
            dumps = DumpZoneData()
            dumpAllHotel(dumps)

            return make_response(SuccessResponse(
                data=dumps.toJson()
            ).toJson(), 300)
        except Exception as e:
            print(e)
            return make_response(FailedResponse(
                errorMessage=str(e)
            ).toJson(), 400)
    
    def post(self):
        """
        Request:
        {
            "hotel_name" - hotel's name
            "address" - hotel's address
            "phone" - hotel's phone number
        }    
        Return
        {
            data: [
                {
                    "hotel_name" - hotel's name
                    "address" - hotel's address
                    "phone" - hotel's phone number
                    "id" - hotel id
                }
            ]
        }
        """
        try:
            req = json.loads(request.form.get("data"))
            if not req:
                raise Exception("Invalid JSON Body")
            
            img = request.files.get("img")
            data = ZoneData(
                name=req.get("hotel_name"),
                address=req.get("address"),
                phone=req.get("phone"),
            )

            registerNewZone(data, img)
            return make_response(SuccessResponse(
                data=[req]
            ).toJson(), 300)
        except Exception as e:
            return make_response(FailedResponse(
                errorMessage=str(e)
            ).toJson(), 400)

@hotel_np.route("/<int:uid>")
class Zone(Resource):
    def post(self, uid):
        """
        Request:
        {
            "zones_id" - Personals' id 
            "name" - room's name
            "desc" - room's descriptions
            "price" - room's price in IDR
            "capacity" - room's capacity
            "img" - room's images (bytes)
            "tags" - tags (list)
        }    
        Return
        {
            data: [
                {
                    "id" - room's package id
                    "zones_id" - Personals' id 
                    "name" - room's name
                    "desc" - room's descriptions
                    "price" - room's price in IDR
                    "capacity" - room's capacity
                    "img" - room's images (url)
                    "tags" - tags (list)
                }
            ]
        }
        """

        try:
            req = json.loads(request.form.get("data"))
            if not req:
                raise Exception("Invalid JSON Body")
            
            img = request.files.get("img")
            data = ItemData(
                zoneId=uid,
                name=req.get("name"),
                desc=req.get("desc"),
                price=req.get("price"),
                capacity=req.get("capacity"),
                tagged=req.get("tags")
            )

            registerNewItem(data, img)
            return make_response(SuccessResponse(
                data=[req]
            ).toJson(), 300)
        except Exception as e:
            print(e)
            return make_response(FailedResponse(
                errorMessage=str(e)
            ).toJson(), 400)
