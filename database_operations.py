import mysql.connector

def establish_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Amritsar@9"
    )

def show_tables(connection, database_name):
    cursor = connection.cursor()
    cursor.execute(f"SHOW TABLES FROM {database_name}")
    tables = [table[0] for table in cursor.fetchall()]
    cursor.close()
    return tables


def fetch_databases(connection):
    cursor = connection.cursor()
    cursor.execute("SHOW DATABASES")
    return [db[0] for db in cursor]

def create_database(connection, database_name):
    cursor = connection.cursor()
    cursor.execute(f"CREATE DATABASE {database_name}")
    print(f"SQL Query: CREATE DATABASE {database_name}")

def use_database(connection, database_name):
    cursor = connection.cursor()
    cursor.execute(f"USE {database_name}")
    print(f"SQL Query: USE {database_name}")

def show_active_database(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT DATABASE()")
    active_db = cursor.fetchone()[0]
    if not active_db:
        active_db = "testing"  # Set default active database to "testing"
    print("Active database:", active_db)
    return active_db

