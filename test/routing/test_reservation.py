from datetime import datetime
import pytz
import hashlib
import requests, json, pytest, os

# Variables
uname = "fuyunaa"
fname = "Lynne"
lname = "Fuyuna"
order_id = 1
product_id = 1
reserve_time_str = "2022-01-01 16:04:20"
reserve_time = datetime.strptime("2022-01-01 16:04:20", 
                "%Y-%m-%d %H:%M:%S")
product_price = 19999999
product_sum = 4
product_name = "Lunar Room"
order_total_price = product_price * product_sum
sign_key = os.urandom(16).hex()

def generateSecureKey(id, total_cost, first_name, last_name, username):
    key = hashlib.sha256()
    key.update(str(id).encode('utf-8'))
    key.update(str(total_cost).encode('utf-8'))
    key.update(f"{first_name}{last_name}".encode('utf-8'))
    key.update(str(username).encode('utf-8'))
    return key.digest().hex()

@pytest.mark.order(5)
@pytest.mark.dependency()
def test_reserve_room():
    data = {
        "username": uname,
        "product_id": product_id,
        "reserved_time": reserve_time_str,
        "sum": product_sum
    }

    res = requests.post("http://localhost:5000/api/book/", headers={
        "ZC-API-TOKEN": "KoreWaABeriSekyurEiPiAiKagiNanoDesu",
        "Content-Type": "application/json"
    }, json=data)

    res_json = res.json()
    assert res_json.get("status") == "OK"
    assert res_json.get("error_message") == None
    assert res_json.get("data") != None

    jsonData = res_json.get("data")[0]
    assert jsonData.get("order_id") == 1
    assert jsonData.get("username") == uname
    assert jsonData.get("product_id") == product_id
    assert jsonData.get("product_name") == product_name
    assert jsonData.get("reserved_time") == reserve_time_str
    assert jsonData.get("total_price") == order_total_price

@pytest.mark.order(5)
@pytest.mark.dependency()
def test_reserve_room_false_username():
    data = {
        "username": "Fuuu",
        "product_id": product_id,
        "reserved_time": reserve_time_str,
        "sum": product_sum
    }

    res = requests.post("http://localhost:5000/api/book/", headers={
        "ZC-API-TOKEN": "KoreWaABeriSekyurEiPiAiKagiNanoDesu",
        "Content-Type": "application/json"
    }, json=data)

    res_json = res.json()
    assert res_json.get("status") == "ERROR"
    assert res_json.get("error_message") == "Invalid Username"
    assert res_json.get("data") == None

@pytest.mark.order(5)
@pytest.mark.dependency()
def test_reserve_room_false_product():
    data = {
        "username": uname,
        "product_id": 5,
        "reserved_time": reserve_time_str,
        "sum": product_sum
    }

    res = requests.post("http://localhost:5000/api/book/", headers={
        "ZC-API-TOKEN": "KoreWaABeriSekyurEiPiAiKagiNanoDesu",
        "Content-Type": "application/json"
    }, json=data)

    res_json = res.json()
    assert res_json.get("status") == "ERROR"
    assert res_json.get("error_message") == "Invalid Product Id"
    assert res_json.get("data") == None

@pytest.mark.order(5)
@pytest.mark.dependency(depends=["test_reserve_room"])
def test_get_order_info():
    res = requests.get(f"http://localhost:5000/api/book/{uname}", headers={
        "ZC-API-TOKEN": "KoreWaABeriSekyurEiPiAiKagiNanoDesu",
        "Content-Type": "application/json"
    })

    res_json = res.json()
    assert res_json.get("status") == "OK"
    assert res_json.get("error_message") == None
    assert res_json.get("data") != None

    jsonData = res_json.get("data")[0]
    assert jsonData.get("username") == uname
    assert jsonData.get("order_id") == 1
    assert jsonData.get("grand_total") == order_total_price
    assert jsonData.get("done") == False
    assert len(jsonData.get("items")) > 0

@pytest.mark.order(5)
@pytest.mark.dependency(depends=["test_reserve_room"])
def test_get_order_info_invalid_username():
    res = requests.get("http://localhost:5000/api/book/Fuuu", headers={
        "ZC-API-TOKEN": "KoreWaABeriSekyurEiPiAiKagiNanoDesu",
        "Content-Type": "application/json"
    })

    res_json = res.json()
    assert res_json.get("status") == "ERROR"
    assert res_json.get("error_message") == "Invalid Username"
    assert res_json.get("data") == None

@pytest.mark.order(4)
@pytest.mark.dependency()
def test_get_order_info_no_orders():
    res = requests.get(f"http://localhost:5000/api/book/{uname}", headers={
        "ZC-API-TOKEN": "KoreWaABeriSekyurEiPiAiKagiNanoDesu",
        "Content-Type": "application/json"
    })

    res_json = res.json()
    assert res_json.get("status") == "ERROR"
    assert res_json.get("error_message") == "Couldn't find any unpaid orders"
    assert res_json.get("data") == None

@pytest.mark.order(6)
@pytest.mark.dependency(depends=["test_reserve_room"])
def test_verify_payment_valid():
    data = {
        "username": uname,
        "first_name": fname,
        "last_name": lname,
        "order_id": order_id,
        "total_price": order_total_price,
        "sign_key": generateSecureKey(order_id, order_total_price, fname, lname, uname)
    }

    res = requests.post(f"http://localhost:5000/api/book/{uname}/pay", headers={
        "ZC-API-TOKEN": "KoreWaABeriSekyurEiPiAiKagiNanoDesu",
        "Content-Type": "application/json"
    }, json=data)

    res_json = res.json()
    assert res_json.get("status") == "OK"
    assert res_json.get("error_message") == None
    assert res_json.get("data") == None

@pytest.mark.order(6)
@pytest.mark.dependency(depends=["test_reserve_room"])
def test_verify_payment_invalid_cost():
    data = {
        "username": uname,
        "first_name": fname,
        "last_name": lname,
        "order_id": order_id,
        "total_price": 928502522,
        "sign_key": generateSecureKey(order_id, 928502522, fname, lname, uname)
    }

    res = requests.post(f"http://localhost:5000/api/book/{uname}/pay", headers={
        "ZC-API-TOKEN": "KoreWaABeriSekyurEiPiAiKagiNanoDesu",
        "Content-Type": "application/json"
    }, json=data)

    res_json = res.json()
    assert res_json.get("status") == "ERROR"
    assert res_json.get("error_message") == "Invalid Sign Key"
    assert res_json.get("data") == None

@pytest.mark.order(6)
@pytest.mark.dependency(depends=["test_reserve_room"])
def test_verify_payment_invalid_first_name():
    data = {
        "username": uname,
        "first_name": "Charlie",
        "last_name": lname,
        "order_id": order_id,
        "total_price": order_total_price,
        "sign_key": generateSecureKey(order_id, order_total_price, fname, lname, uname)
    }

    res = requests.post(f"http://localhost:5000/api/book/{uname}/pay", headers={
        "ZC-API-TOKEN": "KoreWaABeriSekyurEiPiAiKagiNanoDesu",
        "Content-Type": "application/json"
    }, json=data)

    res_json = res.json()
    assert res_json.get("status") == "ERROR"
    assert res_json.get("error_message") == "Invalid Credentials"
    assert res_json.get("data") == None

@pytest.mark.order(6)
@pytest.mark.dependency(depends=["test_reserve_room"])
def test_verify_payment_invalid_last_name():
    data = {
        "username": uname,
        "first_name": fname,
        "last_name": "Musk",
        "order_id": order_id,
        "total_price": order_total_price,
        "sign_key": generateSecureKey(order_id, order_total_price, fname, lname, uname)
    }

    res = requests.post(f"http://localhost:5000/api/book/{uname}/pay", headers={
        "ZC-API-TOKEN": "KoreWaABeriSekyurEiPiAiKagiNanoDesu",
        "Content-Type": "application/json"
    }, json=data)

    res_json = res.json()
    assert res_json.get("status") == "ERROR"
    assert res_json.get("error_message") == "Invalid Credentials"
    assert res_json.get("data") == None

@pytest.mark.order(6)
@pytest.mark.dependency(depends=["test_reserve_room"])
def test_verify_payment_invalid_username():
    data = {
        "username": "fyn15",
        "first_name": fname,
        "last_name": lname,
        "order_id": order_id,
        "total_price": order_total_price,
        "sign_key": generateSecureKey(order_id, order_total_price, fname, lname, uname)
    }

    res = requests.post(f"http://localhost:5000/api/book/fyn15/pay", headers={
        "ZC-API-TOKEN": "KoreWaABeriSekyurEiPiAiKagiNanoDesu",
        "Content-Type": "application/json"
    }, json=data)

    res_json = res.json()
    assert res_json.get("status") == "ERROR"
    assert res_json.get("error_message") == "Invalid Username"
    assert res_json.get("data") == None

@pytest.mark.order(6)
@pytest.mark.dependency(depends=["test_reserve_room"])
def test_verify_payment_invalid_order_id():
    data = {
        "username": uname,
        "first_name": fname,
        "last_name": lname,
        "order_id": 9,
        "total_price": order_total_price,
        "sign_key": generateSecureKey(order_id, order_total_price, fname, lname, uname)
    }

    res = requests.post(f"http://localhost:5000/api/book/{uname}/pay", headers={
        "ZC-API-TOKEN": "KoreWaABeriSekyurEiPiAiKagiNanoDesu",
        "Content-Type": "application/json"
    }, json=data)

    res_json = res.json()
    assert res_json.get("status") == "ERROR"
    assert res_json.get("error_message") == "Invalid Order Id"
    assert res_json.get("data") == None

@pytest.mark.order(7)
@pytest.mark.dependency(depends=["test_reserve_room"])
def test_zone_get_orders():
    res = requests.get("http://localhost:5000/api/zones/1/orders", headers={
        "ZC-API-TOKEN": "KoreWaABeriSekyurEiPiAiKagiNanoDesu",
    })

    res_json = res.json()
    assert res_json.get("status") == "OK"
    assert len(res_json.get("data")) != 0