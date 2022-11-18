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


test("user/reg", {"login": "wex",
                  "name": "Шкарёв Андрей Андреевич",
                  "password": "123123"}, "reg")


token = test("user/auth", {"login": "wex",
                           "password": "123123"}, "auth")[0]
print(token)

test("car/add", {"access_token": token["access_token"],
     "car_info": {"pts": "1234fd"}}, "car add")

cars = (
    test("car/get", {"access_token": token["access_token"]}, "car get"))[0]["result"]


(test("geo/add", {"access_token": "df"}, "geo add fail auth"))

test("geo/add",
     {"access_token": token["access_token"], "car_id": cars[0]["id"], "lat": 12.12, "lon": 96}, "geo add")
