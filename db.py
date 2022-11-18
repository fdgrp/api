import mysql.connector
cnx = mysql.connector.connect(user='user', password='04h608yg435f',
                              port=3333,
                              database='trash', autocouit=True)


def exec(query: str, args: list = []):
    print(query)

    with cnx.cursor() as cursor:
        cursor.execute(query, args)
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
        dt DATETIME DEFAULT CURRENT_TIMESTAMP
        )"""))

    print("ld")
    print(exec("DROP TABLE IF EXISTS CARS"))
    exec("""CREATE TABLE cars (
        id INT NOT NULL AUTO_INCREMENT,
        user_id INT NOT NULL, 
        car_info TEXT,
        PRIMARY KEY (id))""")


init()
