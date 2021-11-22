from __future__ import annotations
from enum import unique

from app.baseModel import db

from dataclasses import dataclass
from datetime import datetime
from typing import List

class Orders(db.Model):
    __tablename__ = "Orders"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, db.ForeignKey("Users.username", ondelete="SET NULL", onupdate="CASCADE"))
    done = db.Column(db.Boolean, default=False)
    total_cost = db.Column(db.Integer, nullable=False, default=0)
    date_created = db.Column(db.DateTime, nullable=False)
    sign_key = db.Column(db.Text, unique=True)

    def insert(self):
        db.session.add(self)
        db.session.commit()
        return self.id
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

class OrderItems(db.Model):
    __tablename__ = "OrderItems"

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("Orders.id", ondelete="SET NULL", onupdate="CASCADE"))
    zone_id = db.Column(db.Integer, db.ForeignKey("Zones.id", ondelete="SET NULL", onupdate="CASCADE"))
    product = db.Column(db.Integer, db.ForeignKey("ZoneItems.id", ondelete="SET NULL", onupdate="CASCADE"))
    reserved_time = db.Column(db.DateTime, nullable=False)
    sum = db.Column(db.Integer, nullable=False)
    total_price=db.Column(db.Integer, nullable=False)

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
class BookedItem:
    productId: int
    reserveTime: datetime
    sum: int
    username: str = None
    orderId: int = None
    productName: str = None
    done: bool = None
    price: int = None
    totalPrice: int = None

    def toJson(cls):
        res = {
            "product_id": cls.productId,
            "reserved_time": datetime.strftime(cls.reserveTime, "%Y-%m-%d %H:%M:%S"),
            "sum": cls.sum
        }

        if cls.username: res["username"] = cls.username
        if cls.orderId: res["order_id"] = cls.orderId
        if cls.productName: res["product_name"] = cls.productName
        if cls.done: res["done"] = cls.done
        if cls.price: res["price"] = cls.price
        if cls.totalPrice: res["total_price"] = cls.totalPrice

        return res

@dataclass
class UserBooks:
    username: str
    orderId: int = None
    sum: int = 0
    grandTotal: int = None
    done: bool = None
    items: List[BookedItem] = None
    sign_key: str = None

    def toJson(cls):
        res = {
            "username": cls.username,
            "order_id": cls.orderId,
            "sum": cls.sum,
            "grand_total": cls.grandTotal,
            "done": cls.done
        }

        if cls.items:
            res["items"] = list(item.toJson() for item in cls.items)
        if cls.sign_key:
            res["sign_key"] = cls.sign_key
        return res

@dataclass
class PayData:
    username: str
    firstName: str
    lastName: str
    orderid: str
    totalPrice: int
    signKey: str