from errors import *
import db
from utils import isempty, domd5, ok

import cfg
import time

import requests


class Geo():
    def places(res):
        res = []
        geos = db.exec("SELECT name, lat, lon FROM places")
        print(geos)
        for geo in geos:
            res.append(Geo.pfrom_tuple(geo))
            
        return Response(200, {"result": res})

    def from_tuple(res):
        return {"car_id": res[0], "lat": res[1], "lon": res[2]}

    def pfrom_tuple(res):
        return {"name": res[0], "lat": res[1], "lon": res[2]}

    def add(req):
        nparams = "lat lon"
        em = isempty(req.data, nparams.split(" "))
        if em:
            return not_specified(em)
        user = Users.get(req)
        if user.code != 200:
            return user
        car = Cars.get_by_id(req)
        if car.code != 200:
            return car
        if car.data['user_id'] != user.data['id'] and not user.data['id'] in cfg.admin_ids:
            return not_allowed()
        db.exec("INSERT INTO geo (car_id, lat, lon) VALUES (%s, %s, %s)",
                car.data['id'], req.data["lat"], req.data["lon"])
        return ok

    def get(req):
        user = Users.get(req)
        if user.code != 200:
            return user
        res = []
        geos = db.exec("SELECT car_id, lat, lon FROM geo WHERE car_id IN (SELECT id FROM cars WHERE user_id=%s)", user.data['id'])
        print(geos)
        for geo in geos:
            res.append(Geo.from_tuple(geo))
            
        return Response(200, {"result": res})
class Cars():

    def from_tuple(res):
        return {"user_id": res[0], "id": res[1], "car_info": res[2]}

    def captcha(req):
        res = requests.get("https://check.gibdd.ru/captcha")
        return Response(res.status_code, res.json())

    def info(req):
        res = requests.post(
            "https://xn--b1afk4ade.xn--90adear.xn--p1ai/proxy/check/auto/history", req.data)

        return Response(403, res.json()) if 200 != res.json().get('status', res.json().get('code')) else Response(200, res.json())

    def edit(req):
        em = isempty(req.data, ["car_info"])
        if em:
            return not_specified(em)
        user = Users.get(req)
        if user.code != 200:
            return user
        car = Cars.get_by_id(req)
        if car.code != 200:
            return car
        if car.data['user_id'] != user.data['id'] and not user.data['id'] in cfg.admin_ids:
            return not_allowed()
        db.exec("UPDATE cars SET car_info = %s WHERE car_id = %s;", req.data['car_info'], car.data['id'] )
        return ok

    def add(req):
        user = Users.get(req)
        if user.code != 200:
            return user
        em = isempty(req.data, ["car_info"])
        if em:
            return not_specified(em)
        db.exec("INSERT INTO cars (user_id, car_info) VALUES (%s, %s)",
                user.data['id'], req.data["car_info"])
        return ok

    def get(req):
        user = Users.get(req)
        if user.code != 200:
            return user

        cars = db.exec(
            "SELECT user_id, id, car_info FROM cars WHERE user_id = %s", user.data['id'],)
        res = []
        for car in cars:
            res.append(Cars.from_tuple(car))
        return Response(200, {"result": res})

    def delete(req):
        user = Users.get(req)
        if user.code != 200:
            return user
        car = Cars.get_by_id(req)
        if car.code != 200:
            return car
        if car.data['user_id'] != user.data['id'] and not user.data['id'] in cfg.admin_ids:
            return not_allowed()

        db.exec("DELETE FROM cars WHERE id = %s", car.data['id'])
        db.exec("DELETE FROM geo WHERE car_id = %s", car.data['id'])
        return ok

    def get_by_id(req):
        em = isempty(req.data, ["car_id"])
        if em:
            return not_specified(em)
        res = db.exec(
            "SELECT user_id, id, car_info FROM cars WHERE id = %s", req.data['car_id'])
        if len(res) > 0:
            res = res[0]
            return Response(200, Cars.from_tuple(res))
        return id_invalid()


class Users():
    def from_tuple(res):
        return {"login": res[0], "id": res[1], "name": res[2]}

    def reg(req):
        nparams = "login name password"
        em = isempty(req.data, nparams.split(" "))
        if em:
            return not_specified(em)

        login, name, password = req.data['login'], req.data['name'], domd5(
            req.data['password'])
        if Users.get_by_login(login):
            return already_used("логин")

        db.exec("INSERT INTO users (login, name, password) VALUES (%s, %s, %s)",
                login, name, password)
        return Users.auth(req)

    def auth(req):
        nparams = "login password"
        em = isempty(req.data, nparams.split(" "))
        if em:
            return not_specified(em)
        res = db.exec("SELECT login, id, name FROM users WHERE login = %s and password = %s",
                      req.data['login'], domd5(req.data["password"]))
        if len(res) > 0:
            res = res[0]
            access_token = domd5(f"{time.time_ns()} {res[0]}")
            db.exec("INSERT INTO auth (user_id, token) VALUES (%s, %s)",
                    res[1], access_token)
            return Response(200, Users.from_tuple(res) | {"access_token": access_token})
        return auth_invalid()

    def get(req):
        nparams = "access_token"
        em = isempty(req.data, nparams.split(" "))
        if em:
            return not_specified(em)
        res = db.exec(
            "SELECT login, id, name FROM users WHERE id = (SELECT user_id FROM auth WHERE token = %s)", req.data['access_token'])
        if len(res) > 0:
            res = res[0]
            return Response(200, Users.from_tuple(res))
        return auth_invalid()

    def get_by_login(login):
        res = db.exec(
            "SELECT id, name, login FROM users WHERE login = %s", login)
        if len(res) > 0:
            return res[0]
