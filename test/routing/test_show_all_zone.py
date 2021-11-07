import requests

def test():
    res = requests.get("http://localhost:5000/api/zones", headers={
        "ZC-API-TOKEN": "KoreWaABeriSekyurEiPiAiKagiNanoDesu",
        "ZC-DEV-KEY": "KyaaMinaiDeKudasaii"
    })

    assert res.status_code != 400
    res_json = res.json()
    assert res_json.get("error_message") == None
    assert res_json.get("data") != None