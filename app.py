from flask import Flask, render_template, request, redirect, session
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'teeheehaha'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Zatanna101_'
app.config['MYSQL_DB'] = 'unstaffeddb'

mysql = MySQL(app)

# Route for the home page
@app.route('/')
def home():
    return render_template('Home.html')

# Route for user login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM unstaffedusers WHERE username = %s AND password = %s",
                    (username, password))
        user = cur.fetchone()
        cur.close()

        if user:
            # User authentication successful
            session['username'] = username
            session['email'] = user['email']
            if user['user_type'] == 'freelancer':
                session['salary'] = user['salary']
                session['location'] = user['location']
                session['skills'] = user['skills']
                session['about_me'] = user['about_me']
            return redirect('/dashboard')  # Redirect to the dashboard page
        else:
            # User authentication failed
            error_message = 'Invalid username or password'
            return render_template('Login.html', error=error_message)

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    # Check if the user is logged in and determine their user type
    if 'username' in session:  # Assuming you are using Flask's session management
        username = session['username']

        # Retrieve the user's data from the database based on their username
        cur = mysql.connection.cursor()
        cur.execute("SELECT user_type FROM unstaffedusers WHERE username = %s", (username,))
        user = cur.fetchone()
        cur.close()

        if user:
            # User data retrieved successfully
            user_type = user[0]
            if user_type == 'freelancer':
                # User is a freelancer
                return render_template('freelance_input.html')
            elif user_type == 'client':
                # User is a user
                return render_template('User_input.html')
            else:
                # User type not recognized
                return redirect('/login')

    # If the user is not logged in or the user type is not recognized, redirect to the login page
    return redirect('/login')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
     if request.method == 'POST':
          user_type = request.form['user_type']
          username = request.form['username']
          password = request.form['password']
          email = request.form['email']
     
          cur = mysql.connection.cursor()
          cur.execute("INSERT INTO unstaffedusers(user_type, username, password, email) VALUES(%s, %s, %s, %s)",
                         (user_type, username, password, email))
          mysql.connection.commit()
          cur.close()
     
          return redirect('/login')
     
     return render_template('Signup.html')

@app.route('/user_profile')
def user_profile():
    username = session['username']
    email = session['email']
    return render_template('User_Profile.html', username=username, email=email)
    

@app.route('/search', methods=['GET', 'POST'])
def search():
        if request.method == 'POST':
            job_type = request.form['job_type']
            location = request.form['location']
            rate = request.form['rate']
            availability = request.form['availability']
            experience = request.form['experience']
            skills = request.form['skills']
        
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO unstaffedjobs(job_type, location, rate, availability, experience, skills) VALUES(%s, %s, %s, %s, %s, %s)",
                            (job_type, location, rate, availability, experience, skills))
            mysql.connection.commit()
            cur.close()
        
            return redirect('/dashboard')
        
        return render_template('FL_Search.html')

@app.route('/freelancer_profile', methods=['GET', 'POST'])
def freelancer_profile():
    if request.method == 'POST':
        name = request.form['name']
        location = request.form['location']
        rate = request.form['rate']
        availability = request.form['availability']
        experience = request.form['experience']
        skills = request.form['skills']
    
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO unstaffedfreelancers(name, location, rate, availability, experience, skills) VALUES(%s, %s, %s, %s, %s, %s)",
                        (name, location, rate, availability, experience, skills))
        mysql.connection.commit()
        cur.close()
    
        return redirect('/dashboard')
    
    return render_template('Freelancer_Profile.html')

@app.route('/user_input', methods=['GET', 'POST'])
def user_profile():
    if request.method == 'POST':
        rate = request.form['rate']
        availability = request.form['availability']
        experience = request.form['experience']
        skills = request.form['skills']
    
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO unstaffedusers(name, location, rate, availability, experience, skills) VALUES(%s, %s, %s, %s, %s, %s)",
                        (name, location, rate, availability, experience, skills))
        mysql.connection.commit()
        cur.close()
    
        return redirect('/dashboard')
    
    return render_template('User_Profile.html')

if __name__ == '__main__':
    app.run()