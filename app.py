from flask import Flask, render_template
import mysql.connector

connection = mysql.connector.connect(
    host='localhost', 
    database='unstaffed', 
    user='root', 
    password='root')

cursor = connection.cursor()

app = Flask(__name__, static_url_path='/static')
app.debug = True

@app.route('/', methods=['GET'])
def home():
    return render_template('Home.html')

@app.route("/Company_login", methods=['GET', 'POST'])
def clogin():
    if flask.request.method == 'GET':
        return render_template('Company_login.html')
    else:
        email = Flask.request.form['email']
        password = Flask.request.form['password']

        # Check if the email and password exist in the User table
        query = "SELECT * FROM User WHERE role = 'company' AND email = %s AND password = %s"
        values = (email, password)
        cursor.execute(query, values)
        result = cursor.fetchone()  # Fetch a single row

        if result:
            # Login successful
            # You can perform additional actions here, such as setting session variables
            return render_template('Company_home.html')
        else:
            # Login failed
            return render_template('Company_login.html', error='Invalid email or password')
        

@app.route("/Freelancer_login", methods=['GET', 'POST'])
def flogin():
    if flask.request.method == 'GET':
        return render_template('Freelancer_login.html')
    else:
        email = flask.request.form['email']
        password = flask.request.form['password']

        # Create a cursor to execute SQL queries
        cursor = connection.cursor()

        # Check if the email and password exist in the User table
        query = "SELECT * FROM User WHERE role = 'freelancer' AND email = %s AND password = %s"
        values = (email, password)
        cursor.execute(query, values)
        result = cursor.fetchone()  # Fetch a single row

        if result:
            # Login successful
            # You can perform additional actions here, such as setting session variables
            return "Login successful"
        else:
            # Login failed
            return "Invalid email or password"

@app.route("/Signup", methods=['GET'])
def signup():
    return render_template('Signup.html')

