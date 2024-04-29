import mysql.connector

def establish_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Amritsar@9",
        #database="testing"
    )

connection = establish_connection()
cursor = connection.cursor()
