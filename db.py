import mysql.connector
cnx = mysql.connector.connect(user="user", password="04h608yg435f",
                              port=3333,
                              database="trash", autocommit=True)

def exec(query: str, args: list = []):
    print(query)
    

    with cnx.cursor() as cursor:
        cursor.execute(query, args)
        result = cursor.fetchall()
        return result



def init():
    print(exec("DROP TABLE if exists users"))
    exec("""create table users (
        id int NOT NULL AUTO_INCREMENT,
        name TEXT NOT NULL,
        login TEXT NOT NULL,
        password TEXT NOT NULL,
        PRIMARY KEY (id))""")


    print(exec("DROP TABLE if exists auth"))
    exec("""create table auth (user_id int, token TEXT)""")
    

    print(exec("DROP TABLE if exists geo"))
    print(exec("""create table geo (
        car_id INT, 
        lat TEXT, 
        lon TEXT, 
        dt DATETIME default CURRENT_TIMESTAMP
        )"""))

    print("ld")
    print(exec("DROP TABLE if exists cars"))
    exec("""create table cars (
        id int NOT NULL AUTO_INCREMENT,
        user_id int not null, 
        car_info TEXT,
        PRIMARY KEY (id))""")


init()
