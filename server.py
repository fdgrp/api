import sbeaver


import models


server = sbeaver.Server("0.0.0.0", 8080, False)

@server.bind("/api/user/reg")
def user_reg(req):
    models.person.from_req(req)

server.start()