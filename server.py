import sbeaver


import models


server = sbeaver.Server("0.0.0.0", 8080, False)

@server.bind("/api/user/reg")
def user_reg(req):
    models.Person.from_req(req)

@server.code500()
def er500(req):
    return {"error": 500}

server.start()