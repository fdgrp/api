import requests


BLUE = "\033[94m"
GREEN = "\033[92m"
RED = "\033[91m"
ENDC = "\033[0m"


def test(method, params={}, msg="task"):
    result = requests.post("http://0.0.0.0:8080/api/"+method, data=params)
    try:
        result = result.json()
    except:
        print(result.text)
        result = {"error": result.text}
    # print(result)
    if "error" in result:
        print(f"{RED}failed {msg}: {result['error']}{ENDC}")
    else:
        print(f"{GREEN}ok {msg}{ENDC}")
    return result, "error" not in result


test("user/reg", {"login": "qwe",
                  "name": "Шкарёв Андрей Андреевич",
                  "password": "qwe"}, "reg")


token = test("user/auth", {"login": "wex",
                           "password": "wexwexwex"}, "auth")[0]['access_token']


user = test("user/get", {"access_token": token}, "get")[0]

test("car/add", {"access_token": token,
     "car_info": {"pts": "1234fd"}}, "car add")

cars = (
    test("car/get", {"access_token": token}, "car get"))[0]["result"]



test("geo/add",
     {"access_token": token, "car_id": cars[0]['id'], "lat": 12.12, "lon": 96}, "geo add")
test("car/del",  {"access_token": token, "car_id": cars[0]['id']}, "car del")

test("car/info",  {"access_token": token, "car_id": cars[0]['id']}, "car info")