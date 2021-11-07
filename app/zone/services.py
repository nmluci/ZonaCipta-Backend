from os import name
from app.zone.models import DumpZoneData, ZoneData, ItemData, ZoneItems
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