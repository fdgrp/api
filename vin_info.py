import base64
import requests
vin = "XWF0AHL35D0019108"


capcha = requests.get("https://check.gibdd.ru/captcha").json()
print(capcha)

with open('c.jpg', 'wb') as f:
    f.write(base64.b64decode(capcha['base64jpg']))
code = input("code: ")
with open("data.json", "w") as f:
    f.write(requests.post("https://xn--b1afk4ade.xn--90adear.xn--p1ai/proxy/check/auto/history",
            {"vin": vin, "checkType": "history", "captchaWord":	code, "captchaToken": capcha['token']}).text)
