import json
import requests

def test():
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
    assert res_json.get("error_message") == None
    assert res_json.get("data") != None

    jsonData = res_json.get("data")[0]
    assert jsonData.get("id") != 0
    assert jsonData.get("hotel_name") == "Lunar Hotel"
    assert jsonData.get("hotel_name") != "LunarHotel"
    assert jsonData.get("address") != "Lunar Sts"
