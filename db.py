import mysql.connector
cnx = mysql.connector.connect(user='user', password='04h608yg435f',
                              port=3333,
                              database='trash')

def exec(query: str, args: list = []):
    print(query)
    
    with cnx.cursor() as cursor:
        cursor.execute(query, args)
        result = cursor.fetchall()
        return result



def init():
    print(exec("DROP TABLE users"))

    exec("""create table users (
        id int NOT NULL AUTO_INCREMENT,
        name TEXT NOT NULL,
        login TEXT NOT NULL,
        PRIMARY KEY (ID))""")

    exec("""create table auth (user_id int, token TEXT)""")

    exec("""create table cars(
        user_id int not null, 
        car_info TEXt
    )""")


try:
    init()
except:
    pass
