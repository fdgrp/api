import db
from sbeaver import Response
import api

class Users():
    def all(req):
        res = []
        users = db.exec(
            "SELECT id, name, login FROM users")
        for user in users:
            res.append(api.Users.from_tuple(user))
        return Response(200, {"result": res})

class Cars():
    def all(req):
        res = []
        cars = db.exec(
            "SELECT user_id, id, car_info FROM cars")
        for car in cars:
            res.append(api.Cars.from_tuple(car))
        return Response(200, {"result": res})
        