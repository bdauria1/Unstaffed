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
def welcome():
    session.clear()
    return render_template('Welcome.html')

@app.route('/home')
def home():
    return render_template('Home.html')

# Route for user login
@app.route('/login', methods=['GET', 'POST'])
def login():
    # If the user is already logged in, redirect to the home page
    if 'username' in session:
        return redirect('/home')

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("SELECT username, email, password, user_type, salary, location, skills, about FROM unstaffedusers WHERE username = %s AND password = %s", (username, password))
        mysql.connection.commit()
        user = cur.fetchone()
        cur.close()

        if user:
            session['username'] = user[0]
            session['email'] = user[1]
            session['password'] = user[2]
            session['user_type'] = user[3]

            if user[3] == 'freelancer':
                session['salary'] = user[4]
                session['location'] = user[5]
                session['skills'] = user[6]
                session['about'] = user[7]
                return redirect('/freelancer_profile')

            return redirect('/user_profile')
        
        return render_template('Login.html', error='Invalid username or password')
    
    return render_template('Login.html')

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

          if user_type == 'freelancer':
               session['salary'] = 0
               session['location'] = ''
               session['skills'] = ''
               session['about'] = ''
     
          return redirect('/login')
     
     return render_template('Signup.html')

@app.route('/user_profile')
def user_profile():
    username = session['username']
    email = session['email']
    return render_template('User.html', username=username, email=email)

@app.route('/user_input', methods=['GET', 'POST'])
def user_input():
    if request.method == 'POST':
        old_username = session['username']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("UPDATE unstaffedusers SET username = %s, email = %s, password = %s WHERE username = %s",
                    (username, email, password, old_username))
        mysql.connection.commit()
        cur.close()

        session['username'] = username
        session['email'] = email
        session['password'] = password

        return redirect('/user_profile')  # Redirect to the user profile page

    return render_template('User_input.html')

@app.route('/freelancer_profile')
def freelancer_profile():
    # Check if the user is logged in and is a freelancer
    if 'username' in session and session.get('user_type') == 'freelancer':
        username = session['username']
        email = session['email']
        salary = session['salary']
        location = session['location']
        skills = session['skills']
        about_me = session['about']

        return render_template('Freelancer.html', username=username, email=email, salary=salary,
                               location=location, skills=skills, about_me=about_me)

    # If the user is not logged in or is not a freelancer, redirect to the login page
    return redirect('/login')

@app.route('/freelancer_input', methods=['GET', 'POST'])
def freelancer_input():
    if request.method == 'POST':
        old_username = session['username']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        salary = request.form['salary']
        location = request.form['location']
        skills = request.form['skills']
        about_me = request.form['about_me']

        cur = mysql.connection.cursor()
        cur.execute("UPDATE unstaffedusers SET username = %s, email = %s, password = %s, salary = %s, location = %s, skills = %s, about = %s WHERE username = %s",
                    (username, email, password, salary, location, skills, about_me, old_username))
        mysql.connection.commit()
        cur.close()

        session['username'] = username
        session['email'] = email
        session['password'] = password
        session['salary'] = salary
        session['location'] = location
        session['skills'] = skills
        session['about'] = about_me  # Update session key to 'about'

        return redirect('/freelancer_profile')
    
    return render_template('Freelancer_input.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        location = request.form['location']
        skills = request.form['skills']
        salary = request.form['salary']

        cur = mysql.connection.cursor()
        cur.execute("SELECT username FROM unstaffedusers WHERE user_type = 'freelancer' AND location = %s AND skills = %s AND salary >= %s ORDER BY salary DESC LIMIT 5",
                    (location, skills, salary))
        results = cur.fetchall()
        mysql.connection.commit()
        cur.close()

        return render_template('Search_results.html', results=results, location=location, skills=skills, salary=salary)

    return render_template('Search.html')

@app.route('/contacts' , methods=['GET', 'POST'])
def contacts():
    if request.method == 'POST':
        username = session['username']

        cur = mysql.connection.cursor()
        cur.execute("SELECT id FROM unstaffedusers WHERE username = %s", (username,))
        user_id = cur.fetchone()

        cur.execute("SELECT person2_id FROM connections WHERE person1_id = %s", (user_id,))
        connections_with_person1 = cur.fetchall()

        # Search for connections where the person is in person2_id column
        cur.execute("SELECT person1_id FROM connections WHERE person2_id = %s", (user_id,))
        connections_with_person2 = cur.fetchall()

        # Combine the results from both queries to get all the connections related to the person
        all_connections = [conn[0] for conn in connections_with_person1 + connections_with_person2]

        connections = []
        
        for connection in all_connections:
            cur.execute("SELECT username FROM unstaffedusers WHERE user_id = %s", (connection,))
            connection_username = cur.fetchone()
            connections.append(connection_username)

        mysql.connection.commit()
        cur.close()

        return render_template('Contacts.html', connections=connections)

    return render_template('Contacts.html')

@app.route('/view_profile/<username>')
def view_profile(username):
    cur = mysql.connection.cursor()
    cur.execute("SELECT username, email, salary, location, skills, about FROM unstaffedusers WHERE username = %s", (username,))
    user = cur.fetchone()
    mysql.connection.commit()
    cur.close()

    return render_template('View_profile.html', user=user)


@app.route('/dashboard')
def dashboard():
    user_type = session['user_type']
    if user_type == 'freelancer':
        return redirect('/freelancer_profile')
    else:
        return redirect('/user_profile')
    
@app.route('/about')
def about():
    return render_template('About_us.html')

@app.route('/feedback')
def feedback():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM posts ORDER BY likes DESC")
    posts = cur.fetchall()
    mysql.connection.commit()
    cur.close()

    return render_template('Feedback.html', posts=posts)

@app.route('/post', methods=['GET', 'POST'])
def post():
    if request.method == 'POST':
        description = session['username'] + ' says: ' + request.form['post']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO posts(post_text, likes) VALUES(%s, 0)", (description,))
        mysql.connection.commit()
        cur.close()

        return redirect('/feedback')
    
    return render_template('Post.html')
    
@app.route('/like/<int:id>')
def like(id):
    cur = mysql.connection.cursor()
    cur.execute("UPDATE posts SET likes = likes + 1 WHERE id = %s", (id,))
    mysql.connection.commit()
    cur.close()

    return redirect('/feedback')

@app.route('/hire/<freelancer_username>', methods=['GET', 'POST'])
def hire():
    if request.method == 'POST':
        client_username = session['username']
        description = request.form['description']
        hourly_fixed = request.form['hourly_fixed']

        cur = mysql.connection.cursor()
        cur.execute("SELECT id FROM unstaffedusers WHERE username = %s", (client_username,))
        client_id = cur.fetchone()

        cur.execute("SELECT id FROM unstaffedusers WHERE username = %s", (freelancer_username,))
        freelancer_id = cur.fetchone()

        cur.execute("INSERT INTO contract(client_id, freelancer_id, description, hourly_fixed) VALUES(%s, %s, %s, %s)",
                    (client_id, freelancer_id, description, hourly_fixed))
        mysql.connection.commit()
        cur.close()

        return redirect('/contracts')
    
    return render_template('Hire.html')      

@app.route('/requests')
def requests():
    freelancer_username = session['username']

    cur = mysql.connection.cursor()
    cur.execute("SELECT id FROM unstaffedusers WHERE username = %s", (freelancer_username,))
    freelancer_id = cur.fetchone()

    cur.execute("SELECT client_id, description, hourlyorfixed FROM contract WHERE freelancer_id = %s", (freelancer_id,))
    requests = cur.fetchall()

    mysql.connection.commit()
    cur.close()

    return render_template('Requests.html', requests=requests)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)