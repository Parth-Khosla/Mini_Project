def create_table(connection, table_name, columns):
    cursor = connection.cursor()
    column_definitions = ", ".join([f"{column_name} {data_type}" for column_name, data_type in columns.items()])
    cursor.execute(f"CREATE TABLE {table_name} ({column_definitions})")
    print(f"SQL Query: CREATE TABLE {table_name} ({column_definitions})")

def drop_table(connection, table_name):
    cursor = connection.cursor()
    cursor.execute(f"DROP TABLE {table_name}")
    print(f"SQL Query: DROP TABLE {table_name}")

def show_tables(connection):
    cursor = connection.cursor()
    cursor.execute("SHOW TABLES")
    tables = [table[0] for table in cursor]
    print(f"In database '{connection.database}', the following tables are present:")
    for table in tables:
        print(table)

def describe_table(connection, table_name):
    cursor = connection.cursor()
    cursor.execute(f"DESC {table_name}")
    table_description = cursor.fetchall()
    print(f"Description of table '{table_name}':")
    for column in table_description:
        print(column)

def select_all_from_table(connection, table_name):
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()
    column_names = [col[0] for col in cursor.description]

    print("| " + " | ".join(column_names) + " |")
    print("|" + "-" * (sum(len(col) + 3 for col in column_names) - 1) + "|")

    for row in rows:
        row_values = [str(value) for value in row]
        print("| " + " | ".join(row_values) + " |")

def insert_into_table(connection, table_name, values):
    cursor = connection.cursor()
    placeholders = ", ".join(["%s"] * len(values))
    cursor.execute(f"INSERT INTO {table_name} VALUES ({placeholders})", values)
    connection.commit()  # Commit the changes
    print(f"SQL Query: INSERT INTO {table_name} VALUES ({placeholders})", values)


def edit_table_value(connection, table_name, column_name, new_value, condition):
    cursor = connection.cursor()
    cursor.execute(f"UPDATE {table_name} SET {column_name} = %s WHERE {condition}", (new_value,))
    print(f"SQL Query: UPDATE {table_name} SET {column_name} = %s WHERE {condition}", (new_value,))

def delete_from_table(connection, table_name, condition):
    cursor = connection.cursor()
    cursor.execute(f"DELETE FROM {table_name} WHERE {condition}")
    print(f"SQL Query: DELETE FROM {table_name} WHERE {condition}")
