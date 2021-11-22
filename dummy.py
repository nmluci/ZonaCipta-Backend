import json, requests

def add_zone(hotel_name, address, phone, imgPath):
    file = {
        "img": open(imgPath, "rb")
    }

    data = {
        "data": json.dumps({
            "hotel_name": hotel_name,
            "address": address,
            "phone": str(phone)
            }).encode("utf-8")
        }
    res = requests.post("http://localhost:5000/api/zones/", headers={
        "ZC-API-TOKEN": "KoreWaABeriSekyurEiPiAiKagiNanoDesu"
    },files=file, data=data)

def add_zone_room(id, room_name, room_desc, room_price, room_cap, tags, imgPath):
    file = {
        "img": open(imgPath, "rb")
    }

    data = {
        "data": json.dumps({
            "zones_id": id, 
            "name": room_name, 
            "desc": room_desc,
            "price": room_price,
            "capacity": room_cap,
            "tags": tags
            }).encode("utf-8")
        }
    res = requests.post("http://localhost:5000/api/zones/1", headers={
        "ZC-API-TOKEN": "KoreWaABeriSekyurEiPiAiKagiNanoDesu"
    },files=file, data=data)

add_zone("Hotel Arts Barcelona", "Barcelona", "0248353905", r"assets/Hotel Arts Barcelona/hotel.png")
add_zone("Hotel Banjarmasin", "Indonesia", "0248353905", r"assets/Hotel Banjarmasin/hotel.jpg")
add_zone("The Executive Centre", "Indonesia", "0248353905", r"assets/The Executive Centre/hotel.jpg")

add_zone_room(1, "Elite", "An Majestic-vibes meeting room personalized for a majestic meet", 15200000, 100, ["Elite"], r"assets/Hotel Arts Barcelona/meeting-room.jpg")
add_zone_room(1, "Business", "An Business class meeting room for business occassion", 280000, 20, ["Elite"], r"assets/Hotel Arts Barcelona/meeting-room.jpg")
add_zone_room(1, "Grand", "An Majestic-vibes meeting room personalized for a majestic meet", 3200000, 200, ["Elite"], r"assets/Hotel Arts Barcelona/meeting-room.jpg")
add_zone_room(2, "Mountain-View", "A Meeting Room", 294000, 30, ["Mountain"], r"assets/Hotel Banjarmasin/meeting-room.jpg")
add_zone_room(2, "Lake-view", "A Meeting Room", 450000, 30, ["Lake"], r"assets/Hotel Banjarmasin/meeting-room.jpg")
add_zone_room(2, "Private Room", "A Meeting Room", 1650000, 30, ["Secrecy"], r"assets/Hotel Banjarmasin/meeting-room.jpg")
