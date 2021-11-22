from __future__ import annotations
from datetime import datetime

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
        if cls.id:
            res["item_id"] = cls.id
        return res

@dataclass
class ZoneData:
    name: str = None
    address: str = None
    phone: int = None
    id: int = None
    img: str = None
    items: list[ItemData] = None

    def toJson(cls):
        res = {
            "hotel_name": cls.name,
            "address": cls.address,
            "phone": cls.phone
        }

        if cls.id: res["id"] = cls.id
        if cls.items: res["items"] = list(x.toJson() for x in cls.items)
        return res

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

@dataclass
class ZoneOrdersData:
    zoneId: int = None
    username: str = None
    orderId: int = None
    productId: int = None
    productName: str = None
    reservedTime: datetime = None
    sum: int = None
    totalPrice: int = None
    
    def toJson(cls):
        return {
            "zone_id": cls.zoneId,
            "username": cls.username,
            "order_id": cls.orderId,
            "product_id": cls.productId,
            "product_name": cls.productName,
            "reserved_time": datetime.strftime(cls.reservedTime, "%Y-%m-%d %H:%M:%S"),
            "sum": cls.sum,
            "total_price": cls.totalPrice
        }

@dataclass
class ZoneOrders:
    zoneId: int
    orders: List[ZoneOrdersData] = None

    def toJson(cls):
        if not cls.orders:
            return None

        return {
            "zone_id": cls.zoneId,
            "orders": list(itm.toJson() for itm in cls.orders)
        }

class QueryType(str):
    def __str__(self) -> str:
        return self.lower()