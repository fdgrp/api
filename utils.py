import hashlib
import sbeaver


def isempty(args, need):
    empty = []
    for key in need:
        name = args.get(key)
        if not name or name == "":
            empty.append(key)
    return empty


def domd5(text):
    return hashlib.sha256(text.encode()).hexdigest()

def cors(*res):

    return sbeaver.Response(res[0], res[1], headers={'Access-Control-Allow-Origin': '*',
                                                     'Access-Control-Allow-Methods': 'GET, POST, OPTIONS, PUT, PATCH, DELETE',
                                                     'Access-Control-Allow-Headers': 'X-Requested-With,content-type',
                                                     'Access-Control-Allow-Credentials': True})
