from flask import Flask
from flask_mysqldb import MySQL
app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'  # MySQL server hostname
app.config['MYSQL_USER'] = 'root'  # MySQL username
app.config['MYSQL_PASSWORD'] = 'root'  # MySQL password
app.config['MYSQL_DB'] = 'eas_gates_solution'  # The name of the database to create
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'  # Cursor class to return results as dictionaries

mysql = MySQL(app)


def initialize_database():
    db_cursor = mysql.connection.cursor()

    # Create the database
    db_cursor.execute("CREATE DATABASE IF NOT EXISTS eas_gates_solution")

    # Select the database
    db_cursor.execute("USE eas_gates_solution")

    # Create tables
    db_cursor.execute("""CREATE TABLE IF NOT EXISTS users(userid INT PRIMARY KEY AUTO_INCREMENT, username VARCHAR(255) NOT NULL,
                      password VARCHAR(255), confirm_password VARCHAR(255), firstname VARCHAR(255), lastname VARCHAR(255),
                      email VARCHAR(255) UNIQUE, phone VARCHAR(15), userrole VARCHAR(255))""")

    db_cursor.execute("""
        CREATE TABLE IF NOT EXISTS userrole (
            roleid INT PRIMARY KEY AUTO_INCREMENT,
            rolename VARCHAR(50) NOT NULL
        )
    """)

    mysql.connection.commit()
    db_cursor.close()

    return 'Database and tables created successfully!'

