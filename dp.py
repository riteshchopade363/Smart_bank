import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="smart_bank",
        auth_plugin='mysql_native_password'
    )
