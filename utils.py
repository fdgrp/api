import hashlib
def isempty(args, need):
    empty = []
    for key in need:
        name = args.get(key)
        if not name or name == '':
            empty.append(key)
    return empty

def domd5(text):
    return hashlib.sha256(text.encode()).hexdigest()

