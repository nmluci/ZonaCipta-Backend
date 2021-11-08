from __future__ import annotations

from typing import Any, List, Dict
from datetime import datetime
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from dataclasses import dataclass
import dotenv

db = SQLAlchemy()
migrate = Migrate()
config = dotenv.load_dotenv()

@dataclass
class SuccessResponse:
    data: List[Any] = None
    count: int = None
    perPage: int = None
    page: int = None
    totalPages: int = None
    created: datetime = None
    
    def toJson(cls):
        if not cls.data: 
            return {
                "status": "OK",
                "date_created": datetime.utcnow()
            }
 
        res = {
            "status": "OK",
            "data": cls.data,
            "count": len(cls.data),
            "date_created": datetime.utcnow()
        }
        if cls.page:
            res["per_page"] = cls.perPage
            res["page"] = cls.page
            # res["totalPages"] = cls.totalPages if cls.totalPages else (cls.count // cls.perPage)
        return res

@dataclass
class FailedResponse:
    errorCode: str = None
    errorMessage: str = None
    created: datetime = None

    def toJson(cls):
        res = {
            "status": "ERROR",
        }
        if cls.errorCode:
            res["error_code"] = cls.errorCode
        elif cls.errorMessage:
            res["error_message"] = cls.errorMessage
        else:
            res["error_message"] = "no specific error returned"
        
        res["date_created"] = datetime.utcnow()
        
        return res
