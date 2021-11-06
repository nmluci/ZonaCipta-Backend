from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from app.baseModel import db

class Hotels(db.Model):
    __tablename__ = "Hotels"

    id = db.Column(db.Integer, primary_key=True)
    hotel_name = db.Column(db.Text, nullable=False)
    address = db.Column(db.Text, nullable=False)
    phone = db.Column(db.Text, nullable=False)

    def insert(self):
        db.session.add(self)
        db.session.commit()
        return self.id
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()
    
class HotelItems(db.Model):
    __tablename__ = "HotelItems"

    id = db.Column(db.Integer, primary_key=True)
    hotel_id = db.Column(db.Integer, db.ForeignKey("Hotels.id", ondelete="SET NULL", onupdate="CASCADE"))
    name = db.Column(db.Text, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)

    def insert(self):
        db.session.add(self)
        db.session.commit()
        return self.id
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

class HotelItemDetails(db.Model):
    __tablename__ = "HotelItemDetails"

    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey("HotelItems.id", ondelete="SET NULL", onupdate="CASCADE"))
    cat_id = db.Column(db.Integer, db.ForeignKey("Categories.id", ondelete="SET NULL", onupdate="CASCADE"))

    def insert(self):
        db.session.add(self)
        db.session.commit()
        return self.id
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

class Category(db.Model):
    __tablename__ = "Categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)

    def insert(self):
        db.session.add(self)
        db.session.commit()
        return self.id
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()
