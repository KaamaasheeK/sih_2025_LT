# import mysql.connector

# def get_connection():
#     connection = mysql.connector.connect(
#         host="localhost",
#         user="root",
#         password="root",
#         database="lt_monitoring"
#     )
#     return connection
import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",   # change if needed
        database="LTline"
    )
