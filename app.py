from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, static_url_path='/static')
app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.Text, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return '<Name %r>' % self.id

@app.route('/')
def home():
    return render_template('Home.html')

@app.route("/Company_login")
def clogin():
    return render_template('Company_login.html')

# Create the database tables
with app.app_context():
    db.create_all()
