from __future__ import annotations

from dataclasses import dataclass
from app.baseModel import db

class Orders(db.Model):
    __tablename__ = "Orders"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, db.ForeignKey("Users.username", ondelete="SET NULL", onupdate="CASCADE"))
    done = db.Column(db.Boolean, default=False)
    total_cost = db.Column(db.Integer, nullable=False, default=0)
    date_created = db.Column(db.DateTime, nullable=False)

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
    product = db.Column(db.Integer, db.ForeignKey("ZoneItems.id", ondelete="SET NULL", onupdate="CASCADE"))
    reserved_time = db.Column(db.DateTime, nullable=False)
    done = db.Column(db.Boolean, default=False)
    sum = db.Column(db.Integer, nullable=False)

    def insert(self):
        db.session.add(self)
        db.session.commit()
        return self.id
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()
