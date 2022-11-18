
def notempty(args, need):
    empty = []
    for key in need:
        name = args.get(key)
        if not name or name == '':
            empty.append(key)
    return empty