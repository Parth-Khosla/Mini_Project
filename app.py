from flask import Flask, render_template, request, jsonify, redirect
import database_operations
from establish_connection_testing import connection
from table_operations import *

app = Flask(__name__)

# Route to render the database operations HTML template
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create_database', methods=['POST'])
def create_database():
    try:
        database_name = request.form['database_name']
        connection = database_operations.establish_connection()
        database_operations.create_database(connection, database_name)
        # No need to close the connection
        return f"Database '{database_name}' created successfully!"
    except Exception as e:
        return str(e)

# Route to use a database
@app.route('/use_database', methods=['POST'])
def use_database():
    try:
        database_name = request.form['database_name']
        connection = database_operations.establish_connection()
        database_operations.use_database(connection, database_name)
        # No need to close the connection
        return f"Database '{database_name}' is now active!"
    except Exception as e:
        return str(e)

# Route to show active database
@app.route('/show_active_database', methods=['GET', 'POST'])
def show_active_database():
    try:
        if request.method == 'POST':
            active_db = request.form['active_database']
        else:
            connection = database_operations.establish_connection()
            active_db = database_operations.show_active_database(connection)
        return render_template('show_active_database.html', active_db=active_db)
    except Exception as e:
        return str(e)

# Route to fetch databases
@app.route('/fetch_databases')
def fetch_databases():
    try:
        connection = database_operations.establish_connection()
        databases = database_operations.fetch_databases(connection)
        # No need to close the connection
        return f"Available databases: {', '.join(databases)}"
    except Exception as e:
        return str(e)

# Route to render the table operations HTML template
@app.route('/table_operations', methods=['GET', 'POST'])
def table_operations():
    if request.method == 'POST':
        try:
            selected_database = request.form.get('selected_database')  # Get the selected database
            selected_table = request.form['selected_table']
            connection = database_operations.establish_connection()
            
            if selected_database:
                database_operations.use_database(connection, selected_database)  # Use the selected database if provided
            else:
                selected_database = 'testing'  # Use the default database "testing" if no database is selected
                database_operations.use_database(connection, selected_database)  # Use the default database

            tables = database_operations.show_tables(connection, selected_database)  # Fetch tables for the selected or default database
            databases = database_operations.fetch_databases(connection)  # Fetch list of databases
            return render_template('table_operations.html', databases=databases, tables=tables)
        except Exception as e:
            return str(e)

    # Fetch list of databases
    connection = database_operations.establish_connection()
    databases = database_operations.fetch_databases(connection)

    return render_template('table_operations.html', databases=databases)

# Route to render the form for creating a table
@app.route('/create_table', methods=['GET', 'POST'])
def create_table_route():
    if request.method == 'POST':
        # Retrieve form data
        table_name = request.form['table_name']
        # Assuming the form data for columns is in a specific format like column1:data_type,column2:data_type
        columns_data = request.form['columns_data']
        columns = {column.split(':')[0]: column.split(':')[1] for column in columns_data.split(',')}
        
        # Call the create_table function
        create_table(connection, table_name, columns)
        
        return redirect('/table_operations')  # Redirect to the table operations page after creating the table
    return render_template('create_table.html')  # Render the form for creating a table

# Route to render the form for dropping a table
@app.route('/drop_table', methods=['GET', 'POST'])
def drop_table_route():
    if request.method == 'POST':
        # Retrieve form data
        table_name = request.form['table_name']
        
        # Call the drop_table function
        drop_table(connection, table_name)
        
        return redirect('/table_operations')  # Redirect to the table operations page after dropping the table
    return render_template('drop_table.html')  # Render the form for dropping a table

# Route to show all tables in the database
@app.route('/show_tables')
def show_tables_route():
    try:
        connection = database_operations.establish_connection()
        active_db = database_operations.show_active_database(connection)  # Get the active database
        tables = database_operations.show_tables(connection, active_db)  # Pass the active database name
        return render_template('show_tables.html', tables=tables)
    except Exception as e:
        return str(e)

# Route to describe a specific table
@app.route('/describe_table/<table_name>')
def describe_table_route(table_name):
    table_description = describe_table(connection, table_name)
    return render_template('describe_table.html', table_name=table_name, table_description=table_description)  # Render the template to describe the table

# Route to select all data from a specific table
@app.route('/select_all/<table_name>')
def select_all_route(table_name):
    table_data = select_all_from_table(connection, table_name)
    return render_template('select_all.html', table_name=table_name, table_data=table_data)  # Render the template to display all data from the table

# Route to render the form for inserting into a table
@app.route('/insert_into_table', methods=['GET', 'POST'])
def insert_into_table_route():
    if request.method == 'POST':
        # Retrieve form data
        table_name = request.form['table_name']
        # Assuming the form data for values is in a specific format like value1,value2,value3
        values = request.form['values'].split(',')
        
        # Call the insert_into_table function
        insert_into_table(table_name, values)
        
        return redirect('/table_operations')  # Redirect to the table operations page after inserting into the table
    return render_template('insert_into_table.html')  # Render the form for inserting into a table

# Route to render the form for editing a table value
@app.route('/edit_table_value', methods=['GET', 'POST'])
def edit_table_value_route():
    if request.method == 'POST':
        # Retrieve form data
        table_name = request.form['table_name']
        column_name = request.form['column_name']
        new_value = request.form['new_value']
        condition = request.form['condition']
        
        # Call the edit_table_value function
        edit_table_value(connection, table_name, column_name, new_value, condition)
        
        return redirect('/table_operations')  # Redirect to the table operations page after editing the table value
    return render_template('edit_table_value.html')  # Render the form for editing a table value

# Route to render the form for deleting from a table
@app.route('/delete_from_table', methods=['GET', 'POST'])
def delete_from_table_route():
    if request.method == 'POST':
        # Retrieve form data
        table_name = request.form['table_name']
        condition = request.form['condition']
        
        # Call the delete_from_table function
        delete_from_table(connection, table_name, condition)
        
        return redirect('/table_operations')  # Redirect to the table operations page after deleting from the table
    return render_template('delete_from_table.html')  # Render the form for deleting from a table


if __name__ == '__main__':
    app.run(debug=True)
