import mysql.connector
cnx = None


def base():
    global cnx
    cnx = mysql.connector.connect(user='user', password='04h608yg435f',
host="new.wanilla.ru",
                              port=3333,
                              database='trash', autocommit=True)
base()
def exec(query: str, args: list = [], req=10):
    print(query)
    try:
        with cnx.cursor() as cursor:
            cursor.execute(query, args)
            result = cursor.fetchall()
            return result
    except mysql.connector.OperationalError:
        base()
        req -= 1
        if req > 0:
            return exec(query, args, req)
        

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
    print(exec("DROP TABLE IF EXISTS cars"))
    exec("""CREATE TABLE cars (
        id INT NOT NULL AUTO_INCREMENT,
        user_id INT NOT NULL, 
        car_info TEXT,
        PRIMARY KEY (id))""")


init()
