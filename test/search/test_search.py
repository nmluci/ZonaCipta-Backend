from _pytest.mark import param
import pytest, json, requests

api = "http://localhost:5000/api/zones/search"

def add_zone(hotel_name, address, phone):
    file = {
        "img": open("./test/018-2.jpg", "rb")
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
    
    return 1

def add_zone_room(id, room_name, room_desc, room_price, room_cap, tags):
    file = {
        "img": open("./test/018-2.jpg", "rb")
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

    return 1

@pytest.mark.order(9)
@pytest.mark.dependency()
def test_search_init():
    assert add_zone("Stellar Hotel", "Main Tubular Ways", "28849840982") == 1
    assert add_zone("Novel Hotel", "Sub Tubular Ways", "29809238535") == 1
    assert add_zone("Stellar Motel", "Sub Tubular Ways", "959037538957") == 1
    assert add_zone("Crux Saki", "Side Nebular Ways", "953579124201") == 1

    assert add_zone_room(1, "Post Gallactical Wars", "A Special Room used by our ancestor pre-human-stellar-wars", 190000, 25, ["stellar", "pre-wars"]) == 1
    assert add_zone_room(1, "Pre Gallactical Wars", "A Special Occasion Room used by Weakling Human on their first time ariving in our beloved world", 290000, 50, ["stellar", "pre-wars", "lowlife"]) == 1
    assert add_zone_room(1, "General Room", "A room suitable for discussing a sensitive topics", 390000, 30, ["privacy"]) == 1
    assert add_zone_room(2, "Post Event Meeting Room", "A Room suitable for light meeting", 420000, 60, ["meeting", "earth"]) == 1
    assert add_zone_room(2, "Mini Hall", "Be Hold, the classic", 530000, 35, ["stellar", "classic"]) == 1
    assert add_zone_room(2, "Dohvahkiin", "Fuz Roh Da", 900000, 125, ["for the worthy", "misc"]) == 1
    assert add_zone_room(3, "Night World", "Ah..", 900000, 125, ["for the ehe", "H"]) == 1
    assert add_zone_room(3, "Midnight World", "Ahh.... yametee", 900000, 125, ["for the ahhh", "H"]) == 1
    assert add_zone_room(3, "Really Really Really Night", "Icchauu", 900000, 125, ["for the ahhhh", "H"]) == 1
    assert add_zone_room(4, "Night World EX", "Slave for saleee", 900000, 125, ["for the ehe", "H"]) == 1
    assert add_zone_room(4, "Midnight World EX", "Cocubine for saleee", 900000, 125, ["for the ahhh", "H"]) == 1
    assert add_zone_room(4, "Really Really Really Night EX", "Well.... here a loli", 900000, 125, ["for the ahhhh", "H"]) == 1


@pytest.mark.order(9)
@pytest.mark.dependency(depends=["test_search_init"])
def test_search_desc():
    res = requests.get(url=api, headers={
        "ZC-API-TOKEN": "KoreWaABeriSekyurEiPiAiKagiNanoDesu"
        }, params={ "query": "ancestor", "per_page": "5", "page": 1 
    }).json()

    print(json.dumps(res, indent=3))
    assert res.get("status") == "OK"
