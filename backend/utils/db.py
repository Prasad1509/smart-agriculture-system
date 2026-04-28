import mysql.connector

def get_db_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Reset@123",   # apna password
        database="smart_agriculture"
    )
    return conn