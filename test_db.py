import mysql.connector

try:
    database = mysql.connector.connect(
        host='localhost',
        user='root',
        password='Mysql875904',
        database='backend_course'
)
    cursor = database.cursor()
    cursor.execute("SELECT DATABASE();")
    record = cursor.fetchone()
    print(f"Connected to database: {record}")
    cursor.close()
    database.close()
except mysql.connector.Error as err:
    print(f"Error: {err}")