import mysql.connector

def connect_db():
    return mysql.connector.connect(
        host="45.171.124.251",
        user="cyg",
        password="Iaad.0301",
        database="iaad"
    )
