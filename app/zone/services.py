from json import dump
from os import name
from app.reservation.models import OrderItems, Orders
from app.user.models import Users
from app.zone.models import DumpZoneData, ZoneData, ItemData, ZoneItems, ZoneOrders, ZoneOrdersData
from app.zone.models import Zones, ZoneItems
from app.baseModel import db

from typing import BinaryIO
import requests as curl

def registerNewZone(metadata: ZoneData, img):
   imgUrl = uploadImg(img)

   zone = Zones(
      name=metadata.name,
      address=metadata.address,
      phone=metadata.phone,
      img=imgUrl
   )
   zone.insert()

   metadata.id = zone.id
   metadata.img = imgUrl

def registerNewItem(metadata: ItemData, img):
   imgUrl = uploadImg(img)

   zoneItem = ZoneItems(
      zones_id=metadata.zoneId,
      name=metadata.name,
      desc=metadata.desc,
      price=metadata.price,
      capacity=metadata.capacity,
      img=imgUrl,
      tags=metadata.tagged,
   )
   zoneItem.insert()
   
   metadata.id = zoneItem.id
   metadata.img = imgUrl

def searchByQuery(query: str, result: DumpZoneData, perPage: int = 25, page: int = 1, ):
   res = db.session.query(ZoneItems).filter(
            ZoneItems.name.ilike(f"%{query}%") | ZoneItems.desc.ilike(f"%{query}%") | ZoneItems.tags.contains([f"{query}"])
         ).limit(perPage).offset(page-1).all()
   
   result.zones = list(ItemData(
      zoneId=itm.zones_id,
      id=itm.id,
      name=itm.name,
      price=itm.price,
      desc=itm.desc,
      capacity=itm.capacity,
      tagged=itm.tags,
      img=itm.img
   ) for itm in res)


def dumpAllHotel(dumps: DumpZoneData):
   data = db.session.query(Zones).all()

   dump = list(ZoneData(
      id=x.id,
      name=x.name, 
      address=x.address,
      phone=x.phone, 
      img=x.img
   ) for x in data)

   dumps.zones = dump

def dumpZoneData(dumps: ZoneData):
   zone = db.session.query(Zones).filter(Zones.id==dumps.id).first()
   items = db.session.query(ZoneItems).filter(ZoneItems.zones_id==zone.id).all()

   dumps.name = zone.name
   dumps.address = zone.address
   dumps.phone = zone.phone
   dumps.img = zone.img
   dumps.items = list(ItemData(
      id=x.id,
      zoneId=zone.id,
      name=x.name, 
      price=x.price,
      desc=x.desc,
      capacity=x.capacity,
      tagged=x.tags,
      img=x.img
   ) for x in items)

def getZoneOrders(dumps: ZoneOrders):
   if not dumps.zoneId:
      raise Exception("zone Id not included")

   zoneData = db.session.query(Zones).filter(Zones.id==dumps.zoneId).first()
   if not zoneData:
      raise Exception("Zone ID isn't valid")

   zoneOrders = db.session.query(OrderItems).filter(OrderItems.zone_id==dumps.zoneId).all()
   if not zoneOrders:
      raise Exception("zone has no orders")
   
   dumps.orders = list(
      ZoneOrdersData(
         zoneId=dumps.zoneId,
         username=db.session.query(Orders).filter(Orders.id==itm.order_id).first().username,
         orderId=itm.order_id,
         productId=itm.product,
         productName=db.session.query(ZoneItems).filter(ZoneItems.id==itm.product).first().name,
         reservedTime=itm.reserved_time
      ) for itm in zoneOrders
   )

def uploadImg(data: BinaryIO):
   res = curl.post("https://api.imgbb.com/1/upload", params={
      'key': '00a1aeca97124c2ddb0ace6f0bc4fffc'
   }, files={
      'image': data.read()
   }).json()

   if res.get("status") == 200:
      return res.get("data").get("url")
   else:
      return None