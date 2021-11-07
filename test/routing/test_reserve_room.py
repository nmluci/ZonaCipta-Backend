import requests
import json

def test():
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

    assert res.status_code != 400, "Response Return HTTP/OK"
    assert res_json.get("error_message") == None, "Response return no error"
    assert res_json.get("data") != None, "Response return data"

    jsonData = res_json.get("data")[0]
    assert jsonData.get("zones_id") != 0
    assert jsonData.get("name") != "Lunar Hotel"
    assert jsonData.get("desc") == "Beautiful"
    assert "Kyaan" in jsonData.get("tags")