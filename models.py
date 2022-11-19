import sbeaver
import db
import utils
import time
from utils import cors


class Pts():
    pass


class Car():
    def __init__(self):
        self.user_id, self.id, self.car_info = None, None, None

    def get(req):
        car_not_in_request = utils.isempty(req.data, ["car_id"])
        if (not car_not_in_request):
            car = db.exec(
                "SELECT user_id, id, car_info FROM cars WHERE ID = %s ", (req.data["car_id"], ))
            exists = len(car) > 0  # check of exists
            if (not exists):
                return 403, {"error": f"Эта машина не принадлежит вам"}
            car = car[0]
            res = Car()
            res.user_id = car[0]
            res.id = car[1]
            res.car_info = car[2]
            return res
        return 403, {"error": f"Оти ключи не заполнены: {car_not_in_request}"}

    def add(req):
        user = Person.auth(req)
        if (user[0] != 200):
            return user
        car_not_in_request = utils.isempty(req.data, ["car_info", ])
        if (not car_not_in_request):
            db.exec("INSERT INTO cars (user_id, car_info) VALUES (%s, %s)",
                    (user[1]['id'], req.data["car_info"]))
            return 200, {"status": "ok"}
        return 403, {"error": f"Эти ключи не заполнены: {car_not_in_request}"}

    def get_all(req):
        user = Person.auth(req)
        if (user[0] != 200):
            return user
        cars = db.exec(
            "SELECT user_id, id, car_info FROM cars WHERE user_id = %s", (user[1]['id'],))
        res = []
        for car in cars:
            pres = Car()
            pres.user_id, pres.id, pres.car_info = car[0], car[1], car[2]
            res.append(pres.__dict__)
        return 200, {"result": res}


class Person():
    def __init__(self):
        self.name, self.login, self.id = None, None, None

    def reg(req) -> tuple:
        reg_not_in_request = utils.isempty(req.data, ["login",
                                                      "name",
                                                      "password", ])

        if (not reg_not_in_request):
            # do hash of password
            pass_hash = utils.domd5(req.data["password"])
            login = req.data["login"]
            name = req.data["name"]

            # check of exists
            exists = len(
                db.exec("SELECT id FROM users WHERE login = %s", (login,))) > 0
            if exists:
                # TODO another languages of error
                return 403, {"error": "Этот логин уже используется. Попробуйте другой"}

            db.exec("INSERT INTO users (login, name, password) VALUES (%s, %s, %s)",
                    (login, name, pass_hash))  # reg user
            empty = utils.isempty(req.data, ["login", "password"])
            if empty:
                return cors(403, {"error": f"Эти ключи не заполнены: {empty}"})
            else:
                login = req.data["login"]
                user = db.exec("SELECT name, id from users WHERE login = %s and password = %s",
                               (login, utils.domd5(req.data["password"])))
                if len(user) < 1:
                    return cors(401, {"error": "Неверный логин или пароль"})
                else:
                    user = user[0]
                    token = utils.domd5(f"{time.time_ns()} {login}")
                    db.exec("INSERT INTO auth (user_id, token) VALUES (%s, %s)",
                            (user[1], token))
                    return 200, {"access_token": token, "name": user[0], "id": user[1]}

        else:
            return 403, {"error": f"Эти ключи не заполнены: {reg_not_in_request}"}

    def auth(req: sbeaver.Request):
        # auth
        token_not_in_request = utils.isempty(req.data, ["access_token"])

        if (not token_not_in_request):  # auth
            token = req.data["access_token"]
            user = db.exec(
                "select name, login, id from users where id=(select user_id from auth where token=%s)", (token,))
            print(user)
            if len(user) < 1:
                return 401, {"error": "Неверный токен"}
            user = user[0]
            res = Person()
            res.name = user[0]
            res.login = user[1]
            res.id = user[2]
            return 200, res.__dict__
        return 403, {"error": f"Эти ключи не заполнены: {token_not_in_request}"}

    def get_by_login(login) -> object:
        user = db.exec(
            "SELECT name, login, id FROM users WHERE login=%s", (login,))[0]
        res = Person()
        res.name = user[0]
        res.login = user[1]
        res.id = user[2]
        return res
