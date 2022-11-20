import sbeaver

from utils import cors
import api, admin


server = sbeaver.Server("0.0.0.0", 8080, False)


@server.bind(r"/(.*)")
def all(req, path):
    print(req)
    res = None
    if path == "api/user/reg":
        res = api.Users.reg(req)
    elif path == "api/user/auth":
        res = api.Users.auth(req)
    elif path == "api/user/get":
        res = api.Users.get(req)

    elif path == "api/car/add":
        res = api.Cars.add(req)
    elif path == "api/car/get":
        res = api.Cars.get(req)
    elif path == "api/car/del":
        res = api.Cars.delete(req)
    elif path == "api/car/info":
        res = api.Cars.info(req)
    elif path == "api/car/captcha":
        res = api.Cars.captcha(req)
    elif path == "api/car/edit":
        res = api.Cars.edit(req)

    elif path == "api/geo/add":
        res = api.Geo.add(req)

    elif path == "admin/user/all":
        res = admin.Users.all(req)
    elif path == "admin/cars/all":
        res = admin.Cars.all(req)

    else:
        res = sbeaver.Response(404, {"error": "Вызван неизевстный метод"})
    return cors(res)


server.start()
