import sbeaver
import utils

class Car():
    def __init__(self, car_number:str, car_mark):
        self.car_number = car_number
        self.car_mark = car_mark

class person():
    def __init__(self, first_name, last_name, bithday, category):
        self.first_name = first_name
        self.last_name = last_name
        self.bithday = bithday
        self.category = category

    def from_req(req: sbeaver.Request):
        # auth
        utils.notempty("acces_token")