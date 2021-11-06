from flask import Flask, request
from flask_cors import CORS
from flask_restx import Api, resource
from app.baseModel import config, db, migrate

def zonaCipta_app():
    app = Flask(__name__)
    app.config["JSON_SORT_KEYS"] = False
    app.config["SQLALCHEMY_TRACK_MODIFICATION"] = True
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
        
    

    api.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)

    return app