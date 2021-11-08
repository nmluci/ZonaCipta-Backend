from os import name
from flask_restx import Namespace, Resource
from flask import request, make_response, jsonify
import json

from app.baseModel import FailedResponse, SuccessResponse, config
from app.zone.models import DumpZoneData, ItemData, QueryType, ZoneData
from app.zone.services import dumpAllHotel, registerNewItem, registerNewZone, searchByQuery

"""
ROUTING

base uri: /api/zones

GET /search - Get a result based on a given query

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
            "status": "OK",
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
            "status": "OK",
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
                data=[data.toJson()]
            ).toJson(), 300)
        except Exception as e:
            print(e)
            return make_response(FailedResponse(
                errorMessage=str(e)
            ).toJson(), 400)

@hotel_np.route("/search")
class SearchZone(Resource):
    def get(self):
        """
        Request:
        params:
            query: query for searching
            per_page: content per page
            page: page nth
        
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
                                    .
                                    .
                                    .
            ]
            page - current page
            perPage - element per page
        }
        """
        try:
            query = request.args.get("query", type=QueryType)
            itemPerPage = request.args.get("per_page", 25, type=int)
            page = request.args.get("page", 1, type=int)

            searchResult = DumpZoneData()
            searchByQuery(query, searchResult, itemPerPage, page)

            return make_response(SuccessResponse(
                data=list(itm.toJson() for itm in searchResult.zones),
                page=page,
                perPage=itemPerPage
            ).toJson(), 300)
            
        except Exception as e:
            print(e)
            return make_response(FailedResponse(
                errorMessage=str(e)
            ).toJson(), 400)
        
@hotel_np.route("/<int:uid>")
class Zone(Resource):
    def get(self):
        """
        Request:
        {
            "perPage" - per page (default=25)
            "page" - page (defauit=1)
            "keywords" - keyword to find
        }

        Return
        {
            "status": "OK",
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
            "status": "OK",
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
                data=[data.toJson()]
            ).toJson(), 300)
        except Exception as e:
            print(e)
            return make_response(FailedResponse(
                errorMessage=str(e)
            ).toJson(), 400)
