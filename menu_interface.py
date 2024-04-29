from database_operations import *
from table_operations import *

def main():
    connection = establish_connection()
    active_db = None

    while True:
        print("\nMain Menu:")
        print("1. Fetch Available Databases")
        print("2. Create Database")
        print("3. Use Database")
        print("4. Show Active Database")
        print("5. Exit Active Database")
        print("6. Table Operations")
        print("7. Exit")

        choice = input("Enter your choice (1-7): ")

        if choice == "1":
            print("Available databases:", fetch_databases(connection))

        elif choice == "2":
            new_db_name = input("Enter name for the new database: ")
            create_database(connection, new_db_name)

        elif choice == "3":
            db_to_use = input("Enter the name of the database you want to use: ")
            use_database(connection, db_to_use)
            active_db = db_to_use

        elif choice == "4":
            if active_db:
                show_active_database(connection)
            else:
                print("No active database selected.")

        elif choice == "5":
            if active_db:
                active_db = None
                print("Exited active database.")
            else:
                print("No active database selected.")

        elif choice == "6":
            if active_db:
                print("\nTable Operations Menu:")
                print("1. Create Table")
                print("2. Drop Table")
                print("3. Show Tables")
                print("4. Describe Table")
                print("5. Select * From Table")
                print("6. Insert Into Table")
                print("7. Edit Table Value")
                print("8. Delete From Table")
                print("9. Back to Main Menu")

                table_choice = input("Enter your choice (1-9): ")

                if table_choice == "1":
                    table_name = input("Enter name for the new table: ")
                    num_columns = int(input("Enter number of columns: "))
                    columns = {}
                    for i in range(num_columns):
                        col_name = input(f"Enter name for column {i + 1}: ")
                        col_type = input(f"Enter data type for column {i + 1}: ")
                        columns[col_name] = col_type
                    create_table(connection, table_name, columns)

                elif table_choice == "2":
                    table_to_drop = input("Enter the name of the table you want to drop: ")
                    drop_table(connection, table_to_drop)

                elif table_choice == "3":
                    show_tables(connection)

                elif table_choice == "4":
                    table_name = input("Enter the name of the table you want to describe: ")
                    describe_table(connection, table_name)

                elif table_choice == "5":
                    table_name = input("Enter the name of the table you want to select data from: ")
                    select_all_from_table(connection, table_name)

                elif table_choice == "6":
                    table_name = input("Enter the name of the table: ")
                    num_values = int(input("Enter the number of values to insert: "))
                    values = [input(f"Enter value {i + 1}: ") for i in range(num_values)]
                    insert_into_table(connection, table_name, values)

                elif table_choice == "7":
                    table_name = input("Enter the name of the table: ")
                    column_name = input("Enter the name of the column to edit: ")
                    new_value = input("Enter the new value: ")
                    condition = input("Enter the condition for selecting the row(s) to edit: ")
                    edit_table_value(connection, table_name, column_name, new_value, condition)

                elif table_choice == "8":
                    table_name = input("Enter the name of the table: ")
                    condition = input("Enter the condition for selecting the row(s) to delete: ")
                    delete_from_table(connection, table_name, condition)

                elif table_choice == "9":
                    continue

                else:
                    print("Invalid choice!")
            else:
                print("Please select an active database first (option 3).")

        elif choice == "7":
            print("Exiting...")
            break

        else:
            print("Invalid choice!")

    connection.close()

if __name__ == "__main__":
    main()
