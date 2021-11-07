from __future__ import annotations

from typing import List
from sqlalchemy.dialects import postgresql
from dataclasses import dataclass

from app.baseModel import db

class Zones(db.Model):
    __tablename__ = "Zones"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    address = db.Column(db.Text, nullable=False)
    phone = db.Column(db.Text, nullable=False)
    img = db.Column(db.Text, nullable=False)

    def insert(self):
        db.session.add(self)
        db.session.commit()
        return self.id
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()
    
class ZoneItems(db.Model):
    __tablename__ = "ZoneItems"

    id = db.Column(db.Integer, primary_key=True)
    zones_id = db.Column(db.Integer, db.ForeignKey("Zones.id", ondelete="SET NULL", onupdate="CASCADE"))
    name = db.Column(db.Text, nullable=False)
    desc = db.Column(db.Text, default=None)
    price = db.Column(db.Integer, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    img = db.Column(db.Text, nullable=False)
    tags = db.Column(postgresql.ARRAY(db.Text), nullable=False)

    def insert(self):
        db.session.add(self)
        db.session.commit()
        return self.id
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

@dataclass
class ItemData:
    zoneId: int
    name: str
    price: int
    desc: int
    price: int
    capacity: str
    tagged: List[str]
    id: int = None
    img: str = None

    def toJson(cls):
        res = {
            "hotel_id": cls.zoneId,
            "name": cls.name,
            "price": cls.price,
            "desc": cls.desc,
            "price": cls.price,
            "capacity": cls.capacity,
            "tagged": cls.tagged 
        }
        
        if cls.img:
            res["img"] = cls.img

        return res

@dataclass
class ZoneData:
    name: str
    address: str
    phone: int
    id: int = None
    img: str = None
    items: list[ItemData] = None

    def toJson(cls):
        res = {
            "name": cls.name,
            "address": cls.address,
            "phone": cls.phone
        }

        if cls.id: res["id"] = cls.id
        if cls.items: res["items"] = list(x.toJson() for x in cls.items)
        return cls

@dataclass
class DumpZoneData:
    zones: List[ZoneData] = None
    count: int = None

    def toJson(cls):
        if not len(cls.zones): return 
        return {
            "zones": list(zone.toJson() for zone in cls.zones),
            "count": len(cls.zones)
        }