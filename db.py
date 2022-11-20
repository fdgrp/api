import cfg

import mysql.connector
cnx = None


def connect():
    global cnx
    cnx = mysql.connector.connect(user=cfg.db_user,
                                  password=cfg.db_password,
                                  host=cfg.db_host,
                                  port=cfg.db_port,
                                  database=cfg.db_name,
                                  autocommit=True)


def exec(query: str, *params):
    with cnx.cursor() as cursor:
        cursor.execute(query, params)
        result = cursor.fetchall()
        return result


def init():
    print(exec("DROP TABLE IF EXISTS users"))
    exec("""create table users (
        id INT NOT NULL AUTO_INCREMENT,
        name TEXT NOT NULL,
        login TEXT NOT NULL,
        password TEXT NOT NULL,
        PRIMARY KEY (id))""")

    print(exec("DROP TABLE IF EXISTS auth"))
    exec("""CREATE TABLE auth (user_id INT, token TEXT)""")

    print(exec("DROP TABLE IF EXISTS geo"))
    print(exec("""CREATE TABLE geo (
        car_id INT, 
        lat TEXT, 
        lon TEXT, 
        dt DATETIME DEFAULT CURRENT_TIMESTAMP)"""))

    print(exec("DROP TABLE IF EXISTS cars"))
    exec("""CREATE TABLE cars (
        id INT NOT NULL AUTO_INCREMENT,
        user_id INT NOT NULL, 
        car_info TEXT,
        PRIMARY KEY (id))""")


connect()
if __name__ == "__main__":
    init()
print(exec("select * from cars where id=%s", 1))