import requests
import json
import pytest

@pytest.mark.order(1)
@pytest.mark.dependency()
def test_add_zone():
    file = {
        "img": open("./test/018-2.jpg", "rb")
    }

    data = {
        "data": json.dumps({
            "hotel_name": "Lunar Hotel",
            "address": "Lunar St.",
            "phone": "3850983531"
            }).encode("utf-8")
        }
    res = requests.post("http://localhost:5000/api/zones/", headers={
        "ZC-API-TOKEN": "KoreWaABeriSekyurEiPiAiKagiNanoDesu"
    },files=file, data=data)

    res_json = res.json()

    assert res.status_code != 400
    assert res_json.get("status") == "OK"
    assert res_json.get("data") != None

    jsonData = res_json.get("data")[0]
    print(res_json.get("data"))
    assert jsonData.get("id") != 0
    assert jsonData.get("hotel_name") == "Lunar Hotel"
    assert jsonData.get("hotel_name") != "LunarHotel"
    assert jsonData.get("address") != "Lunar Sts"

@pytest.mark.order(1)
@pytest.mark.dependency(depends=['test_add_zone'])
def test_add_zone_room():
    file = {
        "img": open("./test/018-2.jpg", "rb")
    }

    data = {
        "data": json.dumps({
            "zones_id": 1, 
            "name": "Lunar Room", 
            "desc": "Beautiful",
            "price": 19999999,
            "capacity": 200,
            "tags": ["Fuee", "Kyaan"]
            }).encode("utf-8")
        }
    res = requests.post("http://localhost:5000/api/zones/1", headers={
        "ZC-API-TOKEN": "KoreWaABeriSekyurEiPiAiKagiNanoDesu"
    },files=file, data=data)

    res_json = res.json()

    assert res.status_code != 400
    assert res_json.get("status") == "OK"
    assert res_json.get("data") != None

    jsonData = res_json.get("data")[0]
    assert jsonData.get("zones_id") != 0
    assert jsonData.get("name") != "Lunar Hotel"
    assert jsonData.get("desc") == "Beautiful"
    assert "Kyaan" in jsonData.get("tagged")

@pytest.mark.order(1)
@pytest.mark.dependency(depends=['test_add_zone'])
def test_show_all_zone():
    res = requests.get("http://localhost:5000/api/zones", headers={
        "ZC-API-TOKEN": "KoreWaABeriSekyurEiPiAiKagiNanoDesu",
        "ZC-DEV-KEY": "KyaaMinaiDeKudasaii"
    })

    assert res.status_code != 400
    res_json = res.json()
    assert res_json.get("status") == "OK"
    assert res_json.get("data") != None

