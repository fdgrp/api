import time
import re

import requests
import sbeaver

import models
import utils
import db
import yandex

server = sbeaver.Server("0.0.0.0", 8080, False)


def cors(*res):
    
    return sbeaver.Response(res[0],res[1],headers={'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS, PUT, PATCH, DELETE',
    'Access-Control-Allow-Headers': 'X-Requested-With,content-type',
    'Access-Control-Allow-Credentials': True})

@server.code500()
def er500(req, path):
    print(req, path)
    return {"error": 500}


@server.bind("/api/user/auth")
def user_auth(req):
    empty = utils.isempty(req.data, ["login", "password"])
    if empty:
        return cors(403, {"error": f"These keys are empty: {empty}"})
    else:
        login = req.data["login"]
        user = db.exec("SELECT name, id from users WHERE login = %s and password = %s",
                       (login, utils.domd5(req.data["password"])))
        if len(user) < 1:
            return cors(401, {"error": "Invalid username or password"})
        else:
            user = user[0]
            token = utils.domd5(f"{time.time_ns()} {login}")
            db.exec("INSERT INTO auth (user_id, token) VALUES (%s, %s)",
                    (user[1], token))
            return cors(200, {"access_token": token, "name": user[0], "id": user[1]})


@server.bind("/api/user/reg")
def user_reg(req):
    return cors(*models.Person.reg(req))


@server.bind("/api/photo/vin")
def get_vin(req: sbeaver.Request):
    for text in yandex.post(req.raw_data):

        if len(text) == 17 and len(re.findall(r"^([^а-я]+)$", text)) == 1:
            return {"result": text}
    return cors(404, {"error": "VIN not recognized"})


@server.bind("/api/car/add")
def car_add(req):
    # if user exists
    return cors(*models.Car.add(req))


@server.bind("/api/car/get")
def car_get(req):
    # if user exists
    return cors(*models.Car.get_all(req))


@server.bind("/api/car/del")
def car_del(req):
    # if user exists
    user = models.Person.auth(req)
    if (type(user) is tuple):
        print("err")
        return cors(*user)
    # if car exisst
    car = models.Car.get(req)
    if (type(car) is tuple):
        print("err")
        return cors(*car)

    # if car belongs this user
    if car.user_id != user.id:
        return cors(403, {"error": "This car doesn`t belong to you"})

    db.exec("delete from cars where id=%s", (car.id,))
    db.exec("delete from geo where car_id=%s", (car.id,))

    return cors(200, {"status": "ok"})



@server.bind("/api/car/captcha")
def captcha(req):
    res = requests.get("https://check.gibdd.ru/captcha")
    return cors(res.status_code, res.json())


@server.bind("/api/car/info")
def car_info(req):
    res = requests.post(
        "https://xn--b1afk4ade.xn--90adear.xn--p1ai/proxy/check/auto/history", req.data)

    return cors(403 if 201 == res.json().get('code') else 200, res.json())



@server.bind("/api/geo/add")
def geo_add(req):
    # if user exists
    user = models.Person.auth(req)
    if (type(user) is tuple):
        print("err")
        return cors(user)
    # if car exisst
    car = models.Car.get(req)
    if (type(car) is tuple):
        print("err")
        return cors(car)
    # if car belongs this user
    if car.user_id != user.id:
        return cors(403, {"error": "This car doesn`t belong to you"})
    # if long and lat correct
    geo_not_in_request = utils.isempty(req.data, ["lon", "lat"])
    if (not geo_not_in_request):
        print(car.__dict__)
        db.exec("INSERT INTO geo (car_id, lat, lon) VALUES (%s, %s, %s)",
                (car.id, req.data["lat"], req.data["lon"]))
        return cors(200, {"status":"ok"})
    return cors(403, {"error": f"These keys are empty: {geo_not_in_request}"})


server.start()
