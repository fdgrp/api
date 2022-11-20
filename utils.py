import hashlib
import sbeaver

ok = sbeaver.Response(200, {"status": "ok"})

def domd5(text):
    return hashlib.sha256(text.encode()).hexdigest()


def isempty(args, need):
    empty = []
    for key in need:
        name = args.get(key)
        if not name or name == "":
            empty.append(key)
    return empty


def cors(res: sbeaver.Response):
    return sbeaver.Response(res.code, res.data, headers={'Access-Control-Allow-Origin': '*',
                                                         'Access-Control-Allow-Methods': 'GET, POST, OPTIONS, PUT, PATCH, DELETE',
                                                         'Access-Control-Allow-Headers': 'X-Requested-With,content-type',
                                                         'Access-Control-Allow-Credentials': True})
