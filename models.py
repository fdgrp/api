import sbeaver
import db
import utils


class Pts():
    pass


class Car():
    def __init__(self):
        self.user_id, self.id, self.car_info = None, None, None

    def get(req):
        car_not_in_request = utils.isempty(req.data, ["car_id"])
        if (not car_not_in_request):
            car = db.exec(
                "select user_id, id, car_info from cars where id = %s ", (req.data['car_id'], ))
            exists = len(car) > 0  # check of exists
            if (not exists):
                return 403, {"error": f"This car not exists"}
            car = car[0]
            res = Car()
            res.user_id = car[0]
            res.id = car[1]
            res.car_info = car[2]
            return res
        return 403, {"error": f"These keys are empty: {car_not_in_request}"}

    def add(req):
        user = Person.auth(req)
        if (type(user) is tuple):
            print("err")
            return user
        car_not_in_request = utils.isempty(req.data, ["car_info", ])
        if (not car_not_in_request):
            db.exec("insert into cars (user_id, car_info) values (%s, %s)",
                    (user.id, req.data['car_info']))
            return {"status": "ok"}
        return 403, {"error": f"These keys are empty: {car_not_in_request}"}

    def get_all(req):
        user = Person.auth(req)
        if (type(user) is tuple):
            print("err")
            return user
        cars = db.exec(
            "select user_id, id, car_info from cars where user_id = %s", (user.id,))
        res = []
        for car in cars:
            pres = Car()
            pres.user_id, pres.id, pres.car_info = car[0], car[1], car[2]
            res.append(pres.__dict__)
        return {"result": res}

class Person():
    def __init__(self):
        self.name, self.login, self.id = None, None, None

    def reg(req):
        reg_not_in_request = utils.isempty(req.data, ["login",
                                                      "name",
                                                      "password", ])

        if (not reg_not_in_request):
            # do hash of password
            pass_hash = utils.domd5(req.data['password'])
            login = req.data['login']
            name = req.data['name']

            # check of exists
            exists = len(
                db.exec("select id from users where login = %s", (login,))) > 0
            if exists:
                # TODO another languages of error
                return 403, {"error": "This login has already been used, try another one"}

            db.exec("insert into users (login, name, password) values (%s, %s, %s)",
                    (login, name, pass_hash))  # reg user

            return 200, Person.get_by_login(login).__dict__

        else:
            return 403, {"error": f"These keys are empty: {reg_not_in_request}"}

    def auth(req: sbeaver.Request):
        # auth
        token_not_in_request = utils.isempty(req.data, ["access_token"])

        if (not token_not_in_request):  # auth
            token = req.data['access_token']
            user = db.exec(
                "select name, login, id from users where id=(select user_id from auth where token=%s)", (token,))
            print(user)
            if len(user) < 1:
                return 401, {"error": "Invalid token"}
            user = user[0]
            res = Person()
            res.name = user[0]
            res.login = user[1]
            res.id = user[2]
            return res

    def get_by_login(login):
        user = db.exec(
            "select name, login, id from users where login=%s", (login,))[0]
        res = Person()
        res.name = user[0]
        res.login = user[1]
        res.id = user[2]
        return res
