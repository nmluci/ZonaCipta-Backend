import requests, json, pytest

@pytest.mark.order(2)
@pytest.mark.dependency()
def test_register_new_user():
    uname = "fuyunaa"
    upass = "KyaanPass"
    fname = "Lynne"
    lname = "Fuyuna"
    email = "lfyn@example.nebula"

    data = {
        "username": uname,
        "password": upass,
        "first_name": fname,
        "last_name": lname,
        "email": email
    }

    res = requests.post("http://localhost:5000/api/users/", headers={
        "ZC-API-TOKEN": "KoreWaABeriSekyurEiPiAiKagiNanoDesu",
        "ZC-DEV-KEY": "KyaaMinaiDeKudasaii",
        "Content-Type": "application/json"
    }, json=data)

    res_json = res.json()

    assert res_json.get("status") == "OK"
    assert res_json.get("error_message") == None
    assert res_json.get("data") != None
    assert res_json.get("data")[0].get("username") == uname, 'Username same as registered'
    assert res_json.get("data")[0].get("password") != upass, 'password properly hashed'
    assert res_json.get("data")[0].get("email") == email, 'email same as registered'

    print(json.dumps(res_json, indent=3))

@pytest.mark.order(2)
@pytest.mark.dependency(depends=['test_register_new_user'])
def test_register_new_user_email_exists():
    uname = "Kuyuna"
    upass = "Ewwuww"
    fname = "Lynne"
    lname = "Fuyuna"
    email = "lfyn@example.nebula"

    data = {
        "username": uname,
        "password": upass,
        "first_name": fname,
        "last_name": lname,
        "email": email
    }

    res = requests.post("http://localhost:5000/api/users/", headers={
        "ZC-API-TOKEN": "KoreWaABeriSekyurEiPiAiKagiNanoDesu",
        "ZC-DEV-KEY": "KyaaMinaiDeKudasaii",
        "Content-Type": "application/json"
    }, json=data)

    res_json = res.json()

    assert res_json.get("status") == "ERROR"
    assert res_json.get("error_message") == "email already registered"
    assert res_json.get("data") == None
    
    print(json.dumps(res_json, indent=3))

@pytest.mark.order(2)
@pytest.mark.dependency(depends=['test_register_new_user'])
def test_register_new_user_username_exists():
    uname = "fuyunaa"
    upass = "Ewwuww"
    fname = "Lynne"
    lname = "Fuyuna"
    email = "lfyn@mail.nebula"

    data = {
        "username": uname,
        "password": upass,
        "first_name": fname,
        "last_name": lname,
        "email": email
    }

    res = requests.post("http://localhost:5000/api/users/", headers={
        "ZC-API-TOKEN": "KoreWaABeriSekyurEiPiAiKagiNanoDesu",
        "ZC-DEV-KEY": "KyaaMinaiDeKudasaii",
        "Content-Type": "application/json"
    }, json=data)

    res_json = res.json()

    assert res_json.get("status") == "ERROR"
    assert res_json.get("error_message") == "username already used"
    assert res_json.get("data") == None
    
    print(json.dumps(res_json, indent=3))

@pytest.mark.order(3)
@pytest.mark.dependency()
def test_sign_in():
    uname = "fuyunaa"
    upass = "KyaanPass"
    fname = "Lynne"
    lname = "Fuyuna"
    email = "lfyn@example.nebula"

    data = {
        "username": uname,
        "password": upass,
    }

    res = requests.post("http://localhost:5000/api/users/auth", headers={
        "ZC-API-TOKEN": "KoreWaABeriSekyurEiPiAiKagiNanoDesu",
        "Content-Type": "application/json"
    }, json=data)

    res_json = res.json()

    assert res_json.get("status") == "OK"
    assert res_json.get("error_message") == None
    assert res_json.get("data") != None

    data = res_json.get("data")[0]
    assert data.get("id") != 0
    assert data.get("username") == uname
    assert data.get("first_name") == fname
    assert data.get("last_name") == lname
    assert data.get("email") == email

@pytest.mark.order(3)
@pytest.mark.dependency()
def test_sign_in_false_username():
    uname = "Kuyuna"
    upass = "KyaanPass"
    fname = "Lynne"
    lname = "Fuyuna"
    email = "lfyn@example.nebula"

    data = {
        "username": uname,
        "password": upass,
    }

    res = requests.post("http://localhost:5000/api/users/auth", headers={
        "ZC-API-TOKEN": "KoreWaABeriSekyurEiPiAiKagiNanoDesu",
        "Content-Type": "application/json"
    }, json=data)

    res_json = res.json()

    assert res_json.get("status") == "ERROR"
    assert res_json.get("error_message") == "username isn't existed"
    assert res_json.get("data") == None

@pytest.mark.order(3)
@pytest.mark.dependency()
def test_sign_in_false_password():
    uname = "fuyunaa"
    upass = "Ewwweaew"
    fname = "Lynne"
    lname = "Fuyuna"
    email = "lfyn@example.nebula"

    data = {
        "username": uname,
        "password": upass,
    }

    res = requests.post("http://localhost:5000/api/users/auth", headers={
        "ZC-API-TOKEN": "KoreWaABeriSekyurEiPiAiKagiNanoDesu",
        "Content-Type": "application/json"
    }, json=data)

    res_json = res.json()

    assert res_json.get("status") == "ERROR"
    assert res_json.get("error_message") == "Invalid Credentials"
    assert res_json.get("data") == None