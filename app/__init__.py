from flask import Flask, request
from flask_cors import CORS
from flask_restx import Api, resource
from app.baseModel import config, db, migrate

from app.hotel.controllers import hotel_np
from app.reservation.controllers import reservation_np

from app.hotel.models import Hotels, HotelItems, HotelItemDetails
from app.reservation.models import OrderItems, Orders


def zonaCipta_app(do_migrate=False):
    app = Flask(__name__)
    app.config["JSON_SORT_KEYS"] = False
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = config.get("DB_AUTH")
    CORS(app)

    api = Api(
        title="ZonaCipta Backend",
        version="1.0b",
        prefix="/api",
        doc="/api/docs"
    )

    @app.before_request
    def headerCheck():
        apiKey = request.headers.get("ZC-API-TOKEN", None)
        if (not apiKey) or apiKey != config.get("API_KEY"):
            return "THOU SHALT NOT PASS"
    
    api.add_namespace(hotel_np)
    api.add_namespace(reservation_np)
    
    api.init_app(app)
    db.init_app(app)

    if do_migrate:
        migrate.init_app(app, db)
        db.drop_all(app=app)
        db.create_all(app=app)
    return app