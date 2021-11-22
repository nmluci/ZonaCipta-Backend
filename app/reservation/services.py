from __future__ import annotations
from datetime import datetime
from itertools import product

from app.reservation.models import Orders, OrderItems, PayData, UserBooks
from app.reservation.models import BookedItem
from app.zone.models import ZoneItems
from app.baseModel import db, config
from app.user.models import Users

import hashlib

def bookNewRoom(metadata: BookedItem):
    user = db.session.query(Users).filter(Users.username==metadata.username).first()
    if not user:
        raise Exception("Invalid Username")

    productItem = db.session.query(ZoneItems).filter(ZoneItems.id==metadata.productId).first()
    if not productItem:
        raise Exception("Invalid Product Id")

    metadata.productName = productItem.name
    metadata.price = productItem.price
    metadata.totalPrice = metadata.price * metadata.sum
    metadata.done = False

    bookingData = db.session.query(Orders).filter(
        (Orders.username==metadata.username) & (Orders.done==False)).first()
    
    if bookingData:
        bookingData.total_cost += metadata.totalPrice
        bookingData.sign_key = generateSignKey(bookingData.id, metadata.totalPrice, 
                                                user.first_name, user.last_name, metadata.username)
        bookingData.update()
        metadata.orderId=bookingData.id
    else:
        bookingData = Orders(
            username=metadata.username, 
            done=False, 
            total_cost=metadata.totalPrice,
            date_created=datetime.utcnow()
        )
        metadata.orderId = bookingData.insert()
        bookingData.sign_key = generateSignKey(bookingData.id, metadata.totalPrice, 
                                                user.first_name, user.last_name, metadata.username)
        bookingData.update()

    newOrderItem = OrderItems(
        order_id=metadata.orderId,
        zone_id=productItem.zones_id,
        product=metadata.productId,
        reserved_time=metadata.reserveTime,
        sum=metadata.sum,
        total_price=metadata.totalPrice
    )
    newOrderItem.insert()

def getUserBooking(metadata: UserBooks):
    if not db.session.query(Users).filter(Users.username==metadata.username).first():
        raise Exception("Invalid Username")
    

    bookingData = db.session.query(Orders).filter(
        (Orders.username==metadata.username) & (Orders.done==False)).first()
    if not bookingData:
        raise Exception("Couldn't find any unpaid orders")
    else:
        metadata.orderId = bookingData.id
        metadata.grandTotal = bookingData.total_cost
        metadata.done = bookingData.done

    bookingItem = db.session.query(OrderItems).filter(
        (OrderItems.order_id==bookingData.id)).all()

    if not bookingItem:
        raise Exception("Couldn't find any item in the order")
    else:
        metadata.items = list(BookedItem(
            productId=item.id,
            productName=db.session.query(ZoneItems).filter(ZoneItems.id==item.id).first().name,
            reserveTime=item.reserved_time,
            price=db.session.query(ZoneItems).filter(ZoneItems.id==item.id).first().price,
            sum=item.sum,
            totalPrice=item.total_price
        ) for item in bookingItem)

def verifyPayment(metadata: PayData) -> bool:
    user = db.session.query(Users).filter(Users.username==metadata.username).first()
    if not user:
        raise Exception("Invalid Username")

    if (user.first_name != metadata.firstName) or (user.last_name != metadata.lastName):
        raise Exception("Invalid Credentials")

    order = db.session.query(Orders).filter(Orders.id==metadata.orderid).first()
    if not order:
        raise Exception("Invalid Order Id")

    return order.sign_key == metadata.signKey
    
def generateSignKey(order_id: int, total_cost: int, first_name:str, last_name: str, username: str):
    secureKey = hashlib.sha256()
    secureKey.update(str(order_id).encode("utf-8"))
    secureKey.update(str(total_cost).encode("utf-8"))
    secureKey.update(f"{first_name}{last_name}".encode("utf-8"))
    secureKey.update(username.encode("utf-8"))
    return secureKey.digest().hex()
