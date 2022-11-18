import sbeaver
import db
import utils


class Pts():
    pass

class Car():
    def __init__(self, car_number: str, car_mark):
        self.car_number = car_number
        self.car_mark = car_mark


class Person():
    def __init__(self, first_name, last_name, category, patronymic, insurance_id, password):
        self.first_name = first_name
        self.last_name = last_name
        self.patronymic = patronymic
        self.category = category
        self.insurance_id = insurance_id
        self.password = password

    def save_to_db(self):
        db.exec("insert into users (first_name, last_name, category, patronymic, insurance_id, password) values (%s, %s, %s, %s, %s)", (self.first_name,
                                                                                                                              self.last_name,
                                                                                                                              self.category,
                                                                                                                              self.patronymic,
                                                                                                                              self.insurance_id,
                                                                                                                              utils.domd5(self.password)))

    def from_req(req: sbeaver.Request):
        # auth
        token_in_request = utils.isempty(req.data, ["access_token"])
        reg_in_request = utils.isempty(req.data, ["first_name",
                                                  "last_name",
                                                  "patronymic",
                                                  "category",
                                                  "insurance_id", "password"])

        print(token_in_request)
        print(reg_in_request)
        if (not token_in_request):  # auth
            token = req.data['access_token']

        elif (not reg_in_request):
            user = Person(**req.data)
            user.save_to_()
            print(user.__dict__)
        else:
            print()
