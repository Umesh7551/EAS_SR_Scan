# Import Nesessary libraries
import datetime
# from datetime import datetime
import json
import os
import time
from flask_mail import Mail, Message
import pandas as pd
import secrets
import string
from flask import Flask, render_template, flash, url_for, request, redirect, session, jsonify, \
    send_from_directory
from flask_session import Session
import re
from functools import wraps
from flask import abort, g
import MySQLdb
import mysql.connector
# import logging
# from flask_mysqldb import MySQL
import MySQLdb.cursors
from threading import Thread
from create_db_tbl import *
# from apscheduler.schedulers.background import BackgroundScheduler
# Create an instance of Flask class
app = Flask(__name__)


# Configure Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465  # Replace with your mail server's port
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'umesh.h@exceloid.com'
app.config['MAIL_PASSWORD'] = 'Hindole@7551'
app.config['MAIL_DEFAULT_SENDER'] = 'umesh.h@exceloid.com'


# Initialize Flask-Mail
mail = Mail(app)
# Application Configuration
app.config['DEBUG'] = True
app.secret_key = 'khj387u2348yhwe723487iudhjwh8e472ye8we7ie872368u48ry87jhe423h3kl5h3l5k,5h35k3hkjmnb5j3hm'
# app.config['SESSION_TYPE'] = 'filesystem'
# app.config['SESSION_FILE_DIR'] = '/sessions'  # Change to your desired directory

# Set session timeout to 30 seconds
# app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(seconds=30)

# Session(app)
# Set up MySQL connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'eas_gates_solution'

mysql = MySQL(app)

# Sample roles with their permissions
ROLES = {
    'admin': {'permissions': ['dashboard', 'config', 'export_report', 'get_report', 'print_data']},
    'storemanager': {'permissions': ['dashboard', 'view_store']},
    'dailymanager': {'permissions': ['dashboard']},
    'shiftlead': {'permissions': ['dashboard']},
    'storeadmin': {'permissions': ['dashboard']},
    'developer': {'permissions': ['dashboard']},
    'senior developer': {'permissions': ['dashboard']},
    'manager': {'permissions': ['dashboard']},
    'shiftmanager': {'permissions': ['dashboard']},
    # ... Add more roles and their permissions as needed
}

def check_unbilled_entries(email, store_id, cc_emails=("hindole.umesh@yahoo.com",)):
# def check_unbilled_entries(email, store_id):
    with app.app_context():
        try:
            # Connect to the MySQL database
            db = MySQLdb.connect(host='localhost', user='root', passwd='root', db='eas_gates_solution')
            cursor = db.cursor()
            # Get the datetime for 20 seconds ago from the current time
            twenty_seconds_ago = datetime.datetime.now() - datetime.timedelta(seconds=20)
            # print(twenty_seconds_ago)
            twenty_seconds_ago_str = twenty_seconds_ago.strftime('%Y-%m-%d %H:%M:%S')
            # print(twenty_seconds_ago_str)
            # print(datetime.datetime.now())
            # Retrieve unbilled entries from the database
            # query = "SELECT id, tag_data, datetime FROM rfid_tag_data WHERE status = 'Unbilled' ORDER BY id DESC"
            # SQL query to get the last unbilled entry within the last 20 seconds
            # query = "SELECT id, tag_data, status FROM rfid_tag_data WHERE status = 'Unbilled' AND STR_TO_DATE(datetime, '%Y-%m-%d %H:%i:%s') >= %s ORDER BY STR_TO_DATE(datetime, '%Y-%m-%d %H:%i:%s') DESC LIMIT 1"
            query = "SELECT id, tag_data, status FROM rfid_tag_data WHERE status = 'Unbilled' AND datetime >= %s ORDER BY datetime DESC LIMIT 1"
            cursor.execute(query, (twenty_seconds_ago_str,))
            unbilled_entries = cursor.fetchone()
            # print(unbilled_entries)
            # Send email to logged-in user if unbilled entries are found
            if unbilled_entries:
                print("User Email ID", email)
                print("CC", cc_emails)
                # Get the email of the logged-in user from the session
                # user_email = session.get('email')  # Replace with the actual key for the user's email in the session
                # user_email = ""  # Replace with the actual key for the user's email in the session
                # print("User Email ID", user_email)
                if email:
                    # Get the store name from the database based on the store_id
                    store_name = get_store_name_from_db(store_id)
                    # print(store_name)
                    # Create the list of recipients, including the primary recipient and CC recipients
                    recipients = [email]
                    recipients.extend(cc_emails)
                    # Send email
                    msg = Message('Unbilled Entries Notification', recipients=recipients, cc=cc_emails)
                    # msg = Message('Unbilled Entries Notification', recipients=[email])
                    msg.body = 'Dear User, there are unbilled entries at your store {}  . Please check your account.'.format(store_name)
                    mail.send(msg)
                    # return "Sent"
            else:
                pass
                # print("No Unbilled Entry")

            # Process unbilled entries (e.g., send them for billing or perform any other action)
            # ...

            # Mark the processed entries as billed
            # for entry in unbilled_entries:
            #     entry_id = entry[0]
            #     update_query = f"UPDATE rfid_tag_data SET status = 'Billed' WHERE id = {entry_id}"
            #     cursor.execute(update_query)
            #     db.commit()

                # Close the database connection
                db.close()

        except Exception as e:
            print("Error occurred while processing unbilled entries:", e)

# @app.route('/check_unbilled', methods=['GET'])
# def run_check_unbilled_entries():
#     check_unbilled_entries()
#     return jsonify({'message': 'Unbilled entries checked successfully.'}), 200

def get_store_name_from_db(store_id):
    # Connect to the database and retrieve the store name based on the store_id
    # Replace the following with your actual database query to get the store name
    db = MySQLdb.connect(host='localhost', user='root', passwd='root', db='eas_gates_solution')
    cursor = db.cursor()
    cursor.execute("SELECT storename FROM stores WHERE storeid = %s", (store_id,))
    store_data = cursor.fetchone()
    # print(store_data)
    db.close()

    if store_data:
        return store_data[0]
    else:
        return "Unknown Store"

def get_user_name_from_db(user_id):
    # Connect to the database and retrieve the store name based on the store_id
    # Replace the following with your actual database query to get the store name
    db = MySQLdb.connect(host='localhost', user='root', passwd='root', db='eas_gates_solution')
    cursor = db.cursor()
    cursor.execute("SELECT username FROM users WHERE userid = %s", (user_id,))
    user_data = cursor.fetchone()
    # print(store_data)
    db.close()

    if user_data:
        return user_data[0]
    else:
        return "Unknown User"

def get_role_name_from_db(role_id):
    # Connect to the database and retrieve the store name based on the store_id
    # Replace the following with your actual database query to get the store name
    db = MySQLdb.connect(host='localhost', user='root', passwd='root', db='eas_gates_solution')
    cursor = db.cursor()
    cursor.execute("SELECT rolename FROM roles WHERE roleid = %s", (role_id,))
    role_data = cursor.fetchone()
    # print(store_data)
    db.close()

    if role_data:
        return role_data[0]
    else:
        return "Unknown Role"

def schedule_task(email, store_id):
    while True:
        # store_id = session.get('store')  # Replace with the actual key for the store_id in the session
        # store_id = session.get('store_id')  # Replace with the actual key for the store_id in the session
        check_unbilled_entries(email, store_id)
        time.sleep(20)
################### Python code session Expiration starts here ##########
# @app.before_request
# def update_session_activity():
#     session.permanent = True
#     session.modified = True
#     session['last_activity'] = datetime.datetime.now()
#
# @app.before_request
# def check_session_timeout():
#     if 'last_activity' in session:
#         last_activity = session['last_activity']
#         now = datetime.datetime.now()
#         elapsed_time = now - last_activity
#         if elapsed_time.total_seconds() > 30:
#             session.clear()  # Delete the session
#             return redirect(url_for('session_logout'))
################### Python code session Expiration ends here ##########
@app.route('/session_logout/')
def session_logout():
    return render_template('session_logout.html')
# Main route or Login route or first page route
# @app.route('/')
# @app.route('/login/', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
#         username = request.form['username']
#         password = request.form['password']
#         cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#         cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password,))
#         result = cursor.fetchone()
#         # print(result)
#         if result:
#             # Retrieve the user's role from the result
#             role = result['role_id']
#             store = result['store_id']
#             # print(role)
#             # Check the user's role and redirect accordingly
#             if role == 1:
#                 session['loggedin'] = True
#                 session['userid'] = result['userid']
#                 session['username'] = result['username']
#                 session['password'] = result['password']
#                 session['role'] = result['role_id']
#                 session['store'] = result['store_id']
#                 return redirect(url_for('dashboard'))
#             elif role == 2:
#                 session['loggedin'] = True
#                 session['username'] = result['username']
#                 session['password'] = result['password']
#                 session['role'] = result['role_id']
#                 session['store'] = result['store_id']
#                 return redirect(url_for('dashboard'))
#             elif role == 3:
#                 session['loggedin'] = True
#                 session['username'] = result['username']
#                 session['password'] = result['password']
#                 session['role'] = result['role_id']
#                 session['store'] = result['store_id']
#                 return redirect(url_for('dashboard'))
#             elif role == 4:
#                 session['loggedin'] = True
#                 session['username'] = result['username']
#                 session['password'] = result['password']
#                 session['role'] = result['role_id']
#                 session['store'] = result['store_id']
#                 return redirect(url_for('dashboard'))
#             elif role == 5:
#                 session['loggedin'] = True
#                 session['username'] = result['username']
#                 session['password'] = result['password']
#                 session['role'] = result['role_id']
#                 session['store'] = result['store_id']
#                 return redirect(url_for('dashboard'))
#
#             elif role == 6:
#                 session['loggedin'] = True
#                 session['userid'] = result['userid']
#                 session['username'] = result['username']
#                 session['password'] = result['password']
#                 session['role'] = result['role_id']
#                 session['store'] = result['store_id']
#                 return redirect(url_for('dashboard'))
#             elif role == 7:
#                 session['loggedin'] = True
#                 session['userid'] = result['userid']
#                 session['username'] = result['username']
#                 session['password'] = result['password']
#                 session['role'] = result['role_id']
#                 session['store'] = result['store_id']
#                 return redirect(url_for('dashboard'))
#             elif role == 8:
#                 session['loggedin'] = True
#                 session['userid'] = result['userid']
#                 session['username'] = result['username']
#                 session['password'] = result['password']
#                 session['role'] = result['role_id']
#                 session['store'] = result['store_id']
#                 return redirect(url_for('dashboard'))
#             elif role == 9:
#                 session['loggedin'] = True
#                 session['userid'] = result['userid']
#                 session['username'] = result['username']
#                 session['password'] = result['password']
#                 session['role'] = result['role_id']
#                 session['store'] = result['store_id']
#                 return redirect(url_for('dashboard'))
#             elif role == 10:
#                 session['loggedin'] = True
#                 session['userid'] = result['userid']
#                 session['username'] = result['username']
#                 session['password'] = result['password']
#                 session['role'] = result['role_id']
#                 session['store'] = result['store_id']
#                 return redirect(url_for('dashboard'))
#
#             else:
#                 flash('You have no role assigned by Admin, Please contact Admin', 'login_warning')
#                 return redirect(url_for('login'))
#         else:
#             flash('Please enter valid credentials', 'login_warning')
#             return redirect(url_for('login'))
#     return render_template('login.html')
################## Python code for login into application starts here ################
@app.route('/')
@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        try:
            username = request.form['username']
            password = request.form['password']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password,))
            result = cursor.fetchone()

            if result:
                # Retrieve the user's role from the result
                role = result['role_id']
                store = result['store_id']
                email = result['email']
                if role is None:
                    flash('You have no role assigned. Please contact the administrator.', 'login_warning')
                    return redirect(url_for('login'))

                # Set session variables
                session['loggedin'] = True
                session['username'] = result['username']
                session['password'] = result['password']
                session['role'] = result['role_id']
                session['store'] = result['store_id']
                session['email'] = result['email']
                session['pairing_code'] = result['pairing_code']

                # if role in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, ]:
                if role in range(1, 51):
                    session['userid'] = result['userid']
                    session['store'] = result['store_id']
                    email = session['email']
                    store_id = session['store']
                    # print(store_id)
                    # print(session['email'])
                    # Start the background scheduler after the user logs in
                    scheduler_thread = Thread(target=schedule_task, args=(email, store_id))
                    scheduler_thread.start()

                    # # Log an informational event
                    # logging.info("User logged in: %s", username)
                    # Log the event in the events table
                    event_type = "User Logged In"
                    event_timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    # user_id = result['user_id']  # Replace with the actual key for user_id in the session
                    event_description = "User {} logged in.".format(result['username'].capitalize())

                    # Insert the event record into the events table
                    cursor.execute(
                        "INSERT INTO events (eventname, datetime, description) VALUES (%s, %s, %s)",
                        (event_type, event_timestamp, event_description))
                    cursor.close()
                    mysql.connection.commit()

                return redirect(url_for('dashboard'))
            else:
                flash('Please enter valid credentials', 'login_warning')
                return redirect(url_for('login'))

        except Exception as e:
            # Handle any exceptions that occur during database operations
            flash('An error occurred: {}'.format(str(e)), 'login_warning')
            return redirect(url_for('login'))

    return render_template('login.html')


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('role') != 1:
            print(session.get('role'))
            return redirect(url_for('unauthorized'))
        return f(*args, **kwargs)
    return decorated_function

# @app.route('/dashboard')
# def dashboard():
#     if 'loggedin' in session:
#         role = session['role']
#         store = session['store']
#         # print("Store ID", store)
#         # fetch all rfid tag data from the rfid_tag_data table
#         cursor = mysql.connection.cursor()
#         cursor.execute("SELECT * FROM rfid_tag_data")
#         rfid_tag_data = cursor.fetchall()
#         # print(rfid_tag_data)
#         # fetch all store data from the stores table
#         db_cursor = mysql.connection.cursor()
#         db_cursor.execute("SELECT * FROM stores")
#         stores_data = db_cursor.fetchall()
#         # print(stores_data)
#         number = 1
#         return render_template('dashboard.html', stores_data=stores_data, number=number, rfid_tag_data=rfid_tag_data, role=role, store=store)
#     else:
#         return render_template('session_logout.html')

@app.route('/dashboard')
def dashboard():
    try:
        if 'loggedin' in session:
            role = session['role']
            store = session['store']
            # print(store)
            # fetch all rfid tag data from the rfid_tag_data table
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT * FROM rfid_tag_data ORDER BY id DESC")
            rfid_tag_data = cursor.fetchall()

            # fetch all store data from the stores table
            db_cursor = mysql.connection.cursor()
            db_cursor.execute("SELECT * FROM stores")
            stores_data = db_cursor.fetchall()

            # fetch store count from stores table
            s_cursor = mysql.connection.cursor()
            s_cursor.execute("SELECT COUNT(*) AS total_stores FROM stores;")
            total_stores = s_cursor.fetchall()
            # print("Total Stores", total_stores)

            # fetch tag count from rfid_tag_data table
            t_cursor = mysql.connection.cursor()
            t_cursor.execute("SELECT COUNT(*) AS total_tags FROM rfid_tag_data;")
            total_tags = t_cursor.fetchall()
            # print(total_tags)

            # fetch billed tags from rfid_tag_data table
            bt_cursor = mysql.connection.cursor()
            bt_cursor.execute("SELECT COUNT(*) AS billed_tags FROM rfid_tag_data WHERE status='Billed';")
            billed_tags = bt_cursor.fetchall()
            # print(billed_tags)

            # fetch unbilled tags from rfid_tag_data table
            ub_cursor = mysql.connection.cursor()
            ub_cursor.execute("SELECT COUNT(*) AS unbilled_tags FROM rfid_tag_data WHERE status='Unbilled';")
            unbilled_tags = ub_cursor.fetchall()
            # print(unbilled_tags)
            number = 1

            return render_template('dashboard.html', stores_data=stores_data, number=number, rfid_tag_data=rfid_tag_data, role=role, store=store, total_stores=total_stores, total_tags=total_tags, billed_tags=billed_tags, unbilled_tags=unbilled_tags)
        else:
            return render_template('session_logout.html')

    except Exception as e:
        # Handle the exception
        # You can log the error, display an error message, or redirect to an error page
        print(f"An error occurred: {str(e)}")
        return render_template('error.html')



# @app.route('/config/')
# @admin_required
# def index():
#     if 'loggedin' in session:
#         db_cursor = mysql.connection.cursor()
#         db_cursor.execute("SELECT fullname FROM users")
#         result = db_cursor.fetchall()
#         # print(result)
#         db_cursor.execute("SELECT storeid, storename FROM stores")
#         storeresult = db_cursor.fetchall()
#         # print(storeresult)
#
#         db_cursor.execute("SELECT roleid, rolename FROM roles")
#         roleresult = db_cursor.fetchall()
#         # print(roleresult)
#         db_cursor.execute('SELECT gateno FROM stores')
#         gateresult = db_cursor.fetchall()
#         db_cursor.execute('SELECT readercount FROM stores')
#         readerresult = db_cursor.fetchall()
#         # Retrieve and display users from the database
#         cursor = mysql.connection.cursor()
#         cursor.execute("SELECT * FROM users")
#         users = cursor.fetchall()
#         # print(users)
#         # Retrieve and display stores from the database
#         cursor = mysql.connection.cursor()
#         cursor.execute("SELECT * FROM stores")
#         stores = cursor.fetchall()
#         # print(stores)
#         return render_template('index.html', result=result, storeresult=storeresult, roleresult=roleresult, gateresult=gateresult, readerresult=readerresult, users=users, stores=stores)
#
#     else:
#         # User is not logged in, redirect to the login page
#         return redirect('/login')

@app.route('/config/')
@admin_required
def index():
    try:
        if 'loggedin' in session:
            db_cursor = mysql.connection.cursor()
            db_cursor.execute("SELECT fullname FROM users ORDER BY userid")
            result = db_cursor.fetchall()

            db_cursor.execute("SELECT storeid, storename FROM stores ORDER BY storeid")
            storeresult = db_cursor.fetchall()

            db_cursor.execute("SELECT roleid, rolename, permissions FROM roles ORDER BY roleid")
            roleresult = db_cursor.fetchall()

            db_cursor.execute('SELECT gateno FROM stores ORDER BY storeid')
            gateresult = db_cursor.fetchall()

            db_cursor.execute('SELECT readercount FROM stores')
            readerresult = db_cursor.fetchall()

            # Retrieve and display users from the database
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT * FROM users ORDER BY userid")
            users = cursor.fetchall()

            # Retrieve and display stores from the database
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT * FROM stores ORDER BY storeid")
            stores = cursor.fetchall()

            # Retrieve and Display events from the database
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT * FROM events ORDER BY eventid DESC")
            events = cursor.fetchall()

            return render_template('index.html', result=result, storeresult=storeresult, roleresult=roleresult,
                                   gateresult=gateresult, readerresult=readerresult, users=users, stores=stores, events=events)
        else:
            # User is not logged in, redirect to the login page
            return redirect('/login')
    except Exception as e:
        # Handle any exceptions that occur during the execution
        return 'An error occurred: {}'.format(str(e))

############# Python code for generating random number for connecting rfid reader windows applicaion ########################
characters = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M','N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W','X', 'Y', 'Z']
def generate_random_string(length):
    # Generate a random string of letters and digits of the given length
    characters = string.ascii_letters + string.digits
    return ''.join(secrets.choice(characters) for _ in range(length))

def generate_random_number():
    # Generate the random numbers and letters in the specified format
    random_numbers = generate_random_string(3)
    random_letters = generate_random_string(3)
    return f"{random_numbers}-{random_letters}-STZ"


@app.route('/user_register/', methods=['POST'])
@admin_required
def user_register():
    if 'loggedin' in session:

        if request.method == 'POST' and 'fullname' in request.form and 'username' in request.form and 'password' in request.form and 'email' in request.form:
            fullname = request.form['fullname']
            username = request.form['username']
            password = request.form['password']
            confirm_password = request.form['confirm_password']
            phone = request.form['phone']
            email = request.form['email']
            # role = request.form['role']
            zone = request.form['zone']
            state = request.form['state']
            city = request.form['city']
            designation = request.form['designation']
            empid = request.form['empid']
            field1 = request.form['field1']
            field2 = request.form['field2']

            db_cursor = mysql.connection.cursor()
            db_cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
            account = db_cursor.fetchone()
            # print(account)
            if account:
                flash('Account Email already exists !', 'email_exist')
            # elif password != confirm_password:
            #     flash('Password and Confirm Password do not match!', 'password_mismatch')
            elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                flash('Invalid email address !', 'invalid_email')
            elif not re.match(r'[A-Za-z0-9]+', username):
                flash('Username must contain only characters and numbers !', 'username_match')
            if not username or not password or not confirm_password or not email:
                flash('Please fill out the form !', 'empty_form')
            else:
                random_number = generate_random_number()
                db_cursor.execute('INSERT INTO users (fullname, username, password, confirm_password, phone, email, zone, state, city, designation, empid, field1, field2, pairing_code) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                    (fullname, username, password, confirm_password, phone, email, zone, state, city, designation, empid, field1, field2, random_number))
                # Log the event in the events table
                event_type = "User Register"
                event_timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                # user_id = result['user_id']  # Replace with the actual key for user_id in the session
                event_description = "User {} Registered.".format(username.capitalize())

                # Insert the event record into the events table
                db_cursor.execute(
                    "INSERT INTO events (eventname, datetime, description) VALUES (%s, %s, %s)",
                    (event_type, event_timestamp, event_description))
                db_cursor.close()
                mysql.connection.commit()
                flash('New User Registered Successfully !', 'user_success')
                return redirect(url_for('index'), 200)
        elif request.method == 'POST':
            flash('Please fill out the form !', 'empty_form')
        return render_template('index.html')


@app.route('/delete_record/<int:userid>', methods=['GET', 'POST'])
@admin_required
def delete_record(userid):
    if 'loggedin' in session:
        if userid is not None:
            db_cursor = mysql.connection.cursor()
            db_cursor.execute("DELETE FROM users WHERE userid = %s", (userid,))
            # Log the event in the events table
            event_type = "User Delete."
            event_timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            # user_id = result['user_id']  # Replace with the actual key for user_id in the session
            user_name = get_user_name_from_db(userid)
            event_description = "User {} Deleted.".format(user_name.capitalize())

            # Insert the event record into the events table
            db_cursor.execute(
                "INSERT INTO events (eventname, datetime, description) VALUES (%s, %s, %s)",
                (event_type, event_timestamp, event_description))
            db_cursor.close()
            mysql.connection.commit()
            flash('Record deleted successfully.', 'user_delete_success')
            # return jsonify({'message': 'Record deleted successfully.'})
            return redirect(url_for('index'))
        else:
            flash('Please select a valid record.')
    else:
        flash('Please log in first.')
    return jsonify({'error': 'Unauthorized'})


@app.route('/delete_store/<int:storeid>', methods=['GET', 'POST'])
@admin_required
def delete_store(storeid):
    if 'loggedin' in session:
        if storeid is not None:
            db_cursor = mysql.connection.cursor()
            db_cursor.execute("DELETE FROM stores WHERE storeid = %s", (storeid,))
            # Log the event in the events table
            event_type = "Store Delete."
            event_timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            # user_id = result['user_id']  # Replace with the actual key for user_id in the session
            store_name = get_store_name_from_db(storeid)
            event_description = "Store {} Deleted.".format(store_name.title())

            # Insert the event record into the events table
            db_cursor.execute(
                "INSERT INTO events (eventname, datetime, description) VALUES (%s, %s, %s)",
                (event_type, event_timestamp, event_description))

            db_cursor.close()
            mysql.connection.commit()
            flash('Record deleted successfully.', 'store_delete_success')
            # return jsonify({'message': 'Record deleted successfully.'})
            return redirect(url_for('index'))
        else:
            flash('Please select a valid record.')
    else:
        flash('Please log in first.')
    return jsonify({'error': 'Unauthorized'})


@app.route('/store_register/', methods=['POST'])
@admin_required
def store_register():
    if 'loggedin' in session:
        msg = ''
        if request.method == 'POST' and 'storename' in request.form and 'storecode' in request.form:
            storename = request.form['storename']
            storecode = request.form['storecode']
            gateno = request.form['gateno']
            readercount = request.form['readercount']
            zone = request.form['zone']
            state = request.form['state']
            city = request.form['city']

            if not storename or not storecode or not gateno or not readercount or not zone or not state or not city:
                msg = 'Please fill out the form !'
            else:
                db_cursor = mysql.connection.cursor()
                db_cursor.execute(
                    'INSERT INTO stores (storename, storecode, gateno, readercount, zone, state, city) VALUES (%s, %s, %s, %s, %s, %s, %s)',
                    (storename, storecode, gateno, readercount, zone, state, city))
                mysql.connection.commit()
                msg = 'You have successfully store registered !'
                return redirect(url_for('index'))
        elif request.method == 'POST':
            msg = 'Please fill out the form !'
        return render_template('index.html', msg=msg)


@app.route('/add_role', methods=['POST'])
@admin_required
def add_role():
    if 'loggedin' in session:
        if request.method == 'POST' and 'role' in request.form:
            role = request.form['role']

        if not role:
            flash('Please fill out data in the form')
        else:
            cursor = mysql.connection.cursor()
            cursor.execute('INSERT INTO roles(rolename) VALUES(%s)', (role,))
            mysql.connection.commit()
            flash("Userrole added successfully", 'role_success')
            return redirect(url_for('index'))
    return render_template('index.html')


@app.route('/unauthorized/')
def unauthorized():
    return render_template('404.html')



@app.route('/logout')
def logout():
    cursor = mysql.connection.cursor()
    # Log the event in the events table
    event_type = "User Logged Out"
    event_timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # user_id = result['user_id']  # Replace with the actual key for user_id in the session
    event_description = "User {} logged Out.".format(session['username'].capitalize())

    # Insert the event record into the events table
    cursor.execute(
        "INSERT INTO events (eventname, datetime, description) VALUES (%s, %s, %s)",
        (event_type, event_timestamp, event_description))
    cursor.close()
    mysql.connection.commit()
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    session.pop('rolename', None)
    return redirect(url_for('login'))


@app.route('/sign_up/', methods=['GET', 'POST'])
def sign_up():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM roles')
    userrole = cursor.fetchall()
    print(userrole)
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        phone = request.form['phone']
        userrole = request.form['userrole']
        # initialize_database()

        db_cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        db_cursor.execute('SELECT * FROM users WHERE username = % s', (username,))
        account = db_cursor.fetchone()
        # print(account)
        if account:
            msg = 'Account Email already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
        elif not username or not password or not email:
            msg = 'Please fill out the form !'
        else:
            db_cursor.execute(
                'INSERT INTO users (username, password, confirm_password, firstname, lastname, email, phone, userrole) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)',
                (username, password, confirm_password, firstname, lastname, email, phone, userrole))
            mysql.connection.commit()
            msg = 'You have successfully registered !'
            return redirect(url_for('login'))
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg=msg, userrole=userrole)


@app.route('/change_password/', methods=['GET', 'POST'])
def change_password():
    if 'loggedin' in session:
        if request.method == 'POST':
            username = session['username']
            current_password = request.form['current_password']
            new_password = request.form['new_password']
            confirm_password = request.form['confirm_password']

            # Verify the current password
            cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cur.execute("SELECT * FROM users WHERE username = %s", (username,))
            user = cur.fetchone()
            cur.close()

            if user and user['password'] == current_password:
                if new_password == confirm_password:
                    # Update the password
                    cur = mysql.connection.cursor()
                    cur.execute("UPDATE users SET password = %s WHERE username = %s", (new_password, username,))
                    mysql.connection.commit()
                    cur.close()
                    flash('Password updated successfully!', 'password_success')
                    return redirect(url_for('index'))
                else:
                    flash('New password and confirm password do not match!', 'password_unmatch')
                    return redirect(url_for('index'))
            else:
                return 'Invalid username or password!'

        return render_template('change_password.html')

# code for assigning multiple roles to one user
# @app.route('/assign_role', methods=['POST'])
# def assign_role():
#     if 'loggedin' in session:
#         if request.method == 'POST' and 'user' in request.form and 'roles' in request.form:
#             user = request.form["user"]
#             roles = request.form.getlist('roles[]')
#             print(roles)
#             if user and roles:
#                 db_cursor = mysql.connection.cursor()
#                 # Delete existing role assignments for the user
#                 db_cursor.execute("DELETE FROM users WHERE user_id = %s", (user,))
#                 for role in roles:
#                     db_cursor.execute("UPDATE users SET role_id = %s WHERE fullname = %s", (role, user))
#                     db_cursor.close()
#                 mysql.connection.commit()
#                 return redirect(url_for('index'))
#             else:
#                 flash('Please Select user and role correctly', 'update_fail')
#         return render_template('index.html')
#     return redirect(url_for('login'))

@app.route('/assign_role', methods=['POST'])
@admin_required
def assign_role():
    if 'loggedin' in session:
        if request.method == 'POST' and 'user' in request.form and 'role' in request.form:
            user = request.form["user"]
            role = request.form['role']
            if user and role:
                db_cursor = mysql.connection.cursor()
                role_name = get_role_name_from_db(role)
                db_cursor.execute("UPDATE users SET role_id = %s, rolename = %s WHERE fullname = %s", (role, role_name, user))
                db_cursor.close()
                mysql.connection.commit()
                return redirect(url_for('index'))
            else:
                flash('Please Select user and role correctly', 'update_fail')
        return render_template('index.html')
    return redirect(url_for('login'))

@app.route('/assign_store', methods=['POST'])
@admin_required
def assign_store():
    if 'loggedin' in session:
        if request.method == 'POST' and 'user' in request.form and 'store' in request.form:
            user = request.form["user"]
            store = request.form["store"]
            if user and store:
                db_cursor = mysql.connection.cursor()
                store_name = get_store_name_from_db(store)
                db_cursor.execute("UPDATE users SET store_id = %s, storename = %s WHERE fullname = %s", (store, store_name, user))
                mysql.connection.commit()
                return redirect(url_for('index'))
            else:
                flash('Please Select user and store correctly', 'update_fail')
        return render_template('index.html')

# @app.route("/users")
# def get_users():
#     # Retrieve and display users from the database
#     cursor = mysql.connection.cursor()
#     cursor.execute("SELECT * FROM users")
#     users = cursor.fetchall()
#     print(users)
#     return render_template("index.html", users=users)

@app.route('/update_user/<int:userid>', methods=['POST'])
@admin_required
def update_user(userid):
    msg = ''
    if 'loggedin' in session:
        if request.method == 'POST' and 'fullname' in request.form and 'username' in request.form and 'password' in request.form and 'confirm_password' in request.form and 'phone' in request.form and 'email' in request.form and 'zone' in request.form and 'state' in request.form and 'city' in request.form and 'designation' in request.form and 'empid' in request.form and 'field1' in request.form and 'field2' in request.form:
            fullname = request.form['fullname']
            username = request.form['username']
            password = request.form['password']
            confirm_password = request.form['confirm_password']
            phone = request.form['phone']
            email = request.form['email']
            zone = request.form['zone']
            state = request.form['state']
            city = request.form['city']
            designation = request.form['designation']
            empid = request.form['empid']
            field1 = request.form['field1']
            field2 = request.form['field2']
            # userid = request.form['userid']

            if not re.match(r'[A-Za-z0-9]+', fullname):
                msg = 'Name must contain only characters and numbers!'
            else:
                try:
                    db_cursor = mysql.connection.cursor()
                    query = """
                        UPDATE users 
                        SET fullname = %s, username = %s, password = %s, confirm_password = %s, phone = %s, email = %s, 
                        zone = %s, state = %s, city = %s, designation = %s, empid = %s, field1 = %s, field2 = %s 
                        WHERE userid = %s
                    """
                    values = (fullname, username, password, confirm_password, phone, email, zone, state, city, designation, empid, field1, field2, userid)
                    db_cursor.execute(query, values)
                    db_cursor.close()
                    mysql.connection.commit()
                    flash('User updated!', 'user_update')
                    return redirect(url_for('index'))
                except Exception as e:
                    # Handle the exception here
                    print(f"An error occurred: {str(e)}")
                    flash('An error occurred while updating the user.', 'error')
                    return redirect(url_for('index'))
        else:
            msg = 'Please fill out the form!'
        return render_template("index.html", msg=msg)
    return redirect(url_for('login'))


    # return render_template('edit_user.html')

@app.route('/get_report/', methods=['GET'])
def get_report():
    if 'loggedin' in session:

        fromdate = request.args.get('fromdate')
        todate = request.args.get('todate')

        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        query = "SELECT id, tag_data, datetime, status, storeid, reader_no, gate_no, bill_no FROM rfid_tag_data WHERE datetime >= %s AND datetime <= %s"
        # query = "SELECT * FROM rfid_config_db.rfid_tag_tbl WHERE BETWEEN date_time = %s AND date_time = %s"
        values = (fromdate, todate)
        cur.execute(query, values)
        data = cur.fetchall()
        # print(data)
        cur.close()
        jsondata = json.dumps(data)
        # print(jsondata)
        return jsondata

# below code is used for the exporting table data from fromdate to todate
@app.route('/export_report', methods=['POST'])
def export_report():
    if 'loggedin' in session:
        try:
            fromdate = request.form.get('fromdate')
            todate = request.form.get('todate')
            # print(fromdate, todate)

            cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            query = "SELECT id, tag_data, datetime, status, storeid, reader_no FROM rfid_tag_data WHERE datetime >= %s AND datetime <= %s"
            values = (fromdate, todate)
            cur.execute(query, values)
            data = cur.fetchall()
            # print(data)
            cur.close()

            # Convert table data to a DataFrame
            df = pd.DataFrame(data)

            # Specify the path to the "Downloads" directory
            downloads_directory = os.path.expanduser("~/Downloads")
            # Generate Excel file
            excel_file_path = os.path.join(downloads_directory, 'exported_data.xlsx')
            df.to_excel(excel_file_path, index=False)

            # Return the file name
            return jsonify({'filePath': 'exported_data.xlsx'})

        except Exception as e:
            # Handle the exception and return an error message
            return jsonify({'error': str(e)})

    return render_template('login.html')

@app.route('/<path:filename>')
def download_file(filename):
    return send_from_directory(os.path.expanduser("~/Downloads"), filename, as_attachment=True)

# below code is used for the printing table data from fromdate to todate
# @app.route('/print_data', methods=['POST'])
# def print_data():
#     if 'loggedin' in session:
#         try:
#             fromdate = request.form.get('fromdate')
#             todate = request.form.get('todate')
#             print(fromdate, todate)
#
#             cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#             query = "SELECT id, tag_data, datetime, status, storeid, reader_no FROM rfid_tag_data WHERE datetime >= %s AND datetime <= %s"
#             values = (fromdate, todate)
#             cur.execute(query, values)
#             data = cur.fetchall()
#             print(data)
#             cur.close()
#
#             # Return the data
#             return jsonify({'data': data})
#
#         except Exception as e:
#             # Handle the exception and return an error message
#             return jsonify({'error': str(e)})
#
#     return render_template('login.html')
@app.route('/print_data', methods=['POST'])
def print_data():
    if 'loggedin' in session:
        try:
            fromdate = request.form.get('fromdate')
            todate = request.form.get('todate')

            # Check if fromdate and todate are empty
            if not fromdate or not todate:
                raise ValueError("Both fromdate and todate are required")

            # print(fromdate, todate)

            cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            query = "SELECT id, tag_data, datetime, status, storeid, reader_no FROM rfid_tag_data WHERE datetime >= %s AND datetime <= %s"
            values = (fromdate, todate)
            cur.execute(query, values)
            data = cur.fetchall()
            # print(data)
            cur.close()

            # Return the data
            return jsonify({'data': data})

        except Exception as e:
            # Handle the exception and return an error message
            return jsonify({'error': str(e)})

    return render_template('login.html')


@app.route('/import_store', methods=['POST'])
def import_store():
    file = request.files['storefile']
    if file:
        # Connect to MySQL database
        db = MySQLdb.connect(host=app.config['MYSQL_HOST'], user=app.config['MYSQL_USER'],
                             password=app.config['MYSQL_PASSWORD'], db=app.config['MYSQL_DB'])
        cursor = db.cursor()

        # Read the CSV file
        csv_data = file.read().decode('utf-8')

        # Split the CSV data into rows
        rows = csv_data.split('\n')
        # Skip the first row
        rows = rows[1:]
        # print(rows)
        for row in rows:
            # Skip empty rows
            if not row:
                continue

            # Split each row into columns
            columns = row.split(',')
            # print(columns)
            # Insert the data into the MySQL table
            query = "INSERT INTO stores (storeid, storename, storecode, gateno, readercount, zone, state, city) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(query, tuple(columns))
            db.commit()

        # Close the database connection
        cursor.close()
        db.close()

        return redirect(url_for('index'))
    else:
        return 'No file selected!'


@app.route('/import_user', methods=['POST'])
def import_user():
    file = request.files['userfile']
    if file:
        # Connect to MySQL database
        db = MySQLdb.connect(host=app.config['MYSQL_HOST'], user=app.config['MYSQL_USER'],
                             password=app.config['MYSQL_PASSWORD'], db=app.config['MYSQL_DB'])
        cursor = db.cursor()

        # Read the CSV file
        csv_data = file.read().decode('utf-8')

        # Split the CSV data into rows
        rows = csv_data.split('\n')
        # Skip the first row
        rows = rows[1:]
        # print(rows)
        for row in rows:
            # Skip empty rows
            if not row:
                continue

            # Split each row into columns
            columns = row.split(',')
            # print(columns)
            # Insert the data into the MySQL table
            query = "INSERT INTO users (userid, fullname, username, password, confirm_password, phone, email, zone, state, city, designation, empid, field1, field2) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(query, tuple(columns))
            db.commit()

        # Close the database connection
        cursor.close()
        db.close()

        return redirect(url_for('index'))
    else:
        return 'No file selected!'

# Route to handle the RFID tag information retrieval
# @app.route('/rfid_info/<tag_number>', methods=['GET'])
# def rfid_info(tag_number):
#     if 'loggedin' in session:
#         # Logic to retrieve RFID tag information from the database
#         db_cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#         db_cursor.execute("SELECT id, tag_data, datetime, status, storeid, reader_no FROM rfid_tag_data WHERE tag_data =%s", (tag_number))
#         tag_info = db_cursor.fetchone()
#         # print(tag_info)
#         # The returned data will be a list of list
#         # image_data = tag_info['product_image']
#         # print(image_data)
#         # Decode the string
#
#         # binary_data = base64.b64decode(image_data)
#         # print(binary_data)
#         # Convert the bytes into a PIL image
#         # try:
#         #     image = Image.open(io.BytesIO(binary_data))
#         #     # Convert the image back to a base64-encoded string
#         #     buffered = io.BytesIO()
#         #     image.save(buffered, format='JPEG')
#         #     encoded_image = base64.b64encode(buffered.getvalue()).decode('utf-8')
#         # except PIL.UnidentifiedImageError:
#         #     print("Error: Unable to identify the image file.")
#
#         # Update the 'product_image' field with the base64-encoded string
#         # tag_info['product_image'] = binary_data
#         # print(tag_info)
#         # Replace this with your own implementation
#         return jsonify(tag_info)
#     return redirect(url_for('login'))


# Specify the directory to save the temporary images
# TEMP_IMAGE_DIR = '/images/product_images/'
# #
# @app.route('/rfid_info/<tag_number>', methods=['GET'])
# def rfid_info(tag_number):
#     if 'loggedin' in session:
#         # Logic to retrieve RFID tag information from the database
#         db_cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#         db_cursor.execute("SELECT id, tag_data, datetime, status, storeid, reader_no, product_image FROM rfid_tag_data WHERE tag_data = %s", (tag_number,))
#         tag_info = db_cursor.fetchone()
#
#         if tag_info['product_image']:
#             # Generate a unique filename for the temporary image
#             temp_image_filename = f"{tag_info['id']}.jpg"
#             temp_image_path = os.path.join(TEMP_IMAGE_DIR, temp_image_filename)
#
#             # Create the directory if it doesn't exist
#             os.makedirs(TEMP_IMAGE_DIR, exist_ok=True)
#
#             # Decode the base64-encoded image data
#             binary_image_data = base64.b64decode(tag_info['product_image'])
#
#             # Save the image file
#             with open(temp_image_path, 'wb') as f:
#                 f.write(binary_image_data)
#
#             # Update the 'product_image' field with the temporary image path
#             tag_info['product_image'] = temp_image_path
#
#         return jsonify(tag_info)
#     return redirect(url_for('login'))

# @app.route('/rfid_info/<tag_number>/<row_id>', methods=['GET'])
# def rfid_info(tag_number, row_id):
#     if 'loggedin' in session:
#
#         # Logic to retrieve RFID tag information from the database
#         db_cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#         db_cursor.execute("SELECT id, tag_data, datetime, status, storeid, reader_no, product_image FROM rfid_tag_data WHERE tag_data = %s AND id =%s", (tag_number, row_id))
#         tag_info = db_cursor.fetchone()
#
#         if tag_info['product_image']:
#             # Update the 'product_image' field with the image URL
#             tag_info['product_image'] = '/images/product_images/' + str(tag_info['id']) + '.jpg'
#
#         return jsonify(tag_info)
#     return redirect(url_for('login'))
# Specify the directory to save the temporary images
IMAGE_DIR = '/images/product_images/'
# #
# @app.route('/rfid_info/<row_id>', methods=['GET'])
# def rfid_info(row_id):
#     if 'loggedin' in session:
#         # Logic to retrieve RFID tag information from the database using the row ID
#         db_cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#         db_cursor.execute("SELECT id, tag_data, datetime, status, storeid, reader_no, product_image FROM rfid_tag_data WHERE id = %s", (row_id,))
#         tag_info = db_cursor.fetchone()
#         print(tag_info)
#         if tag_info['product_image']:
#             # Create the directory if it doesn't exist
#             os.makedirs(IMAGE_DIR, exist_ok=True)
#             # Update the 'product_image' field with the image URL
#             # tag_info['product_image'] = '/images/product_images/' + str(tag_info['id']) + '.jpg'
#             tag_info['product_image'] = IMAGE_DIR + row_id + '.jpg'
#
#         return jsonify(tag_info)
#     return redirect(url_for('login'))
#
#
# @app.route('/images/product_images/<filename>')
# def serve_image(filename):
#     return send_from_directory(IMAGE_DIR, filename)
#

########### Working code###############
@app.route('/rfid_info/<row_id>', methods=['GET'])
def rfid_info(row_id):
    if 'loggedin' in session:
        # Logic to retrieve RFID tag information from the database using the row ID
        db_cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        db_cursor.execute("SELECT id, tag_data, datetime, status, storecode, reader_no, product_image FROM rfid_tag_data WHERE id = %s", (row_id,))
        tag_info = db_cursor.fetchone()
        # print(tag_info)
        if tag_info['product_image']:
            # Convert binary image data to JPG or PNG file
            image_data = tag_info['product_image']
            filename = IMAGE_DIR + row_id + '.jpg'  # or 'image_dir + row_id + '.png' for PNG format
            with open(filename, 'wb') as file:
                file.write(image_data)

            # Update the 'product_image' field with the image URL
            tag_info['product_image'] = '/images/product_images/' + row_id + '.jpg'  # or '/images/product_images/' + row_id + '.png' for PNG format

        return jsonify(tag_info)
    return redirect(url_for('login'))


@app.route('/images/product_images/<filename>')
def serve_image(filename):
    return send_from_directory(IMAGE_DIR, filename)


# @app.route('/update_role/<int:roleid>', methods=['POST'])
# @admin_required
# def update_role(roleid):
#     if 'loggedin' in session:
#         if request.method == 'POST' and 'rolename' in request.form:
#             try:
#                 editrole = request.form['rolename']
#                 db_cursor = mysql.connection.cursor()
#                 query = "UPDATE roles SET rolename = %s WHERE roleid = %s"
#                 values = (editrole, roleid)
#                 db_cursor.execute(query, values)
#                 db_cursor.close()
#                 mysql.connection.commit()
#                 return redirect(url_for('index'))
#             except Exception as e:
#                 # Handle the exception here
#                 print(f"An error occurred: {str(e)}")
#                 flash("An error occurred while updating the role.", "error")
#                 return redirect(url_for('index'))
#         else:
#             flash("Invalid request. Please try again.", "error")
#             return redirect(url_for('index'))
#     else:
#         return redirect(url_for('login'))

@app.route('/update_role/<int:roleid>', methods=['GET', 'POST'])
@admin_required
def update_role(roleid):
    print("update_role function called!")
    if 'loggedin' in session:
        if request.method == 'POST' and 'rolename' in request.form and 'permissions' in request.form:
            # try:
            editrole = request.form['rolename']
            print(editrole)
            permissions = request.form.getlist('permissions')
            print(permissions)
            # Serialize the list of permissions to JSON format
            permissions_json = json.dumps(permissions)
            print(permissions_json)
            db_cursor = mysql.connection.cursor()
            query = "UPDATE roles SET permissions = %s WHERE roleid = %s"
            values = (permissions_json, roleid)
            db_cursor.execute(query, values)
            db_cursor.close()
            mysql.connection.commit()
            return redirect(url_for('index'))
            # except Exception as e:
            #     # Handle the exception here
            #     print(f"An error occurred: {str(e)}")
            # flash("An error occurred while updating the role.", "error")
            # return redirect(url_for('index'))
        else:
            flash("Invalid request. Please try again.", "error")
            return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))



@app.route('/update_store/<int:storeid>', methods=['POST'])
def update_store(storeid):
    if 'loggedin' in session:
        if request.method == 'POST' and 'storename' in request.form and 'storecode' in request.form and 'gateno' in request.form and 'readercount' in request.form and 'zone' in request.form and 'state' in request.form and 'city' in request.form:
            try:
                storename = request.form['storename']
                storecode = request.form['storecode']
                gateno = request.form['gateno']
                readercount = request.form['readercount']
                zone = request.form['zone']
                state = request.form['state']
                city = request.form['city']

                db_cursor = mysql.connection.cursor()
                query = "UPDATE stores SET storename = %s, storecode =%s, gateno =%s, readercount =%s, zone =%s, state =%s, city =%s WHERE storeid = %s"
                values = (storename, storecode, gateno, readercount, zone, state, city, storeid)
                db_cursor.execute(query, values)
                db_cursor.close()
                mysql.connection.commit()
                return redirect(url_for('index'))
            except Exception as e:
                # Handle the exception here
                print(f"An error occurred: {str(e)}")
                flash("An error occurred while updating the role.", "error")
                return redirect(url_for('index'))
        else:
            flash("Invalid request. Please try again.", "error")
            return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))
################## Code for getting data based on store name #######################
@app.route('/get_table_data', methods=['GET', 'POST'])
def get_table_data():
    if 'loggedin' in session:
        store_name = request.form['store_name']
        # print(store_name.rstrip())
        db_cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        # query = """SELECT id, tag_data FROM rfid_tag_data INNER JOIN stores ON rfid_tag_data.storecode = stores.storecode WHERE storename = '%s'"""
        #store_name="'"+store_name+"'"+""
        #print(store_name)

        # Execute the query with the storename parameter
        # db_cursor.execute("SELECT rfid_tag_data.id, rfid_tag_data.tag_data FROM rfid_tag_data LEFT JOIN stores ON rfid_tag_data.storecode = stores.storecode WHERE storename = '"+store_name+"'")
        query = "SELECT rfid_tag_data.id, rfid_tag_data.tag_data, rfid_tag_data.datetime, rfid_tag_data.status, rfid_tag_data.storecode, rfid_tag_data.reader_no, rfid_tag_data.gate_no, rfid_tag_data.bill_no FROM rfid_tag_data LEFT JOIN stores ON rfid_tag_data.storecode = stores.storecode WHERE storename = %(storename)s"
        db_cursor.execute(query, {'storename':store_name.rstrip()})
        results = db_cursor.fetchall()
        # for qn in results:
        #     print(qn)
        #
        # Print the results
        # for row in results:
        #     print(f"ID: {row[0]}, Tag Data: {row[1]}")

        #db_cursor.execute("SELECT id, tag_data FROM rfid_tag_data INNER JOIN stores ON rfid_tag_data.storecode = stores.storecode WHERE storename = %s", (store_name,))
        #data = db_cursor.fetchall()
        #print(data)
        # Retrieve table data based on store name
        # ...
        # Return the table data as a list of dictionaries
        return jsonify(results)
    return redirect(url_for('login'))






# def generate_random_code(length=6):
#     characters = string.ascii_letters + string.digits
#     pairing_code = ''.join(secrets.choice(characters) for _ in range(length))
#     return pairing_code
#
# def store_pairing_code(pairing_code, user_id):
#     cursor = mysql.connection.cursor()
#     # Insert the pairing code and user ID into the table
#     cursor.execute('''
#             INSERT INTO pairing_codes (pairing_code, userid) VALUES (%s, %s)
#         ''', (pairing_code, user_id))
#     cursor.close()
#     # Commit the changes and close the connection
#     mysql.connection.commit()
#
#
#
# # Flask route to generate a pairing code
# @app.route('/generate_pairing_code/', methods=['POST'])
# def generate_pairing_code():
#     # Generate a random pairing code
#     pairing_code = generate_random_code()
#
#     # Store the pairing code in the database along with relevant information
#     # store_pairing_code(pairing_code, user_id)
#
#     return jsonify({'pairing_code': pairing_code})


@app.route('/email_config', methods=['POST'])
def email_config():
    if 'loggedin' in session:
        if request.method == 'POST' and 'from_email' in request.form and 'to_email' in request.form:
            pass

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7551)