from sbeaver import Response
def not_specified(params):
    return Response(403, {"error":f"Эти ключи не указаны: {params}"})

def already_used(param):
    return Response(403, {"error": f"Этот {param} уже используется. Попробуйте другой"})

def auth_invalid():
    return Response(401, {"error": f"Неверный логин или пароль"})

def id_invalid():
    return Response(403, {"error": f"Неверный идентификатор"})

def not_allowed():
    return Response(403, {"error": f"Вам не разрешена данная операция"})