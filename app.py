import flask
from flask import Flask, Response, request, render_template, redirect, url_for
from flaskext.mysql import MySQL
import flask_login

# for image uploading
import os, base64

mysql = MySQL()
app = Flask(__name__)
app.secret_key = 'brooke and brandon'  

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'cookie01'
app.config['MYSQL_DATABASE_DB'] = 'photoshare'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

#begin code used for login
login_manager = flask_login.LoginManager()
login_manager.init_app(app)

conn = mysql.connect()
cursor = conn.cursor()
cursor.execute("SELECT email from Users")
users = cursor.fetchall()

def getUserList():
	cursor = conn.cursor()
	cursor.execute("SELECT email from Users")
	return cursor.fetchall()

class User(flask_login.UserMixin):
	pass

@login_manager.user_loader
def user_loader(email):
	users = getUserList()
	if not(email) or email not in str(users):
		return
	user = User()
	user.id = email
	return user

@login_manager.request_loader
def request_loader(request):
	users = getUserList()
	email = request.form.get('email')
	if not(email) or email not in str(users):
		return
	user = User()
	user.id = email
	cursor = mysql.connect().cursor()
	cursor.execute("SELECT password FROM Users WHERE email = '{0}'".format(email))
	data = cursor.fetchall()
	pwd = str(data[0][0] )
	user.is_authenticated = request.form['password'] == pwd
	return user
#############################################################################################

# home page - will let the user either log in or create an account
@app.route("/", methods=['GET'])
def welcome():
    return render_template("welcome.html")


# login page - on success move to hello, on failure more to unauth
@app.route("/login", methods=['GET', 'POST'])
def login():
    if flask.request.method == 'GET':
         return render_template("login.html")
    else: 
         email = flask.request.form['email']
         cursor = conn.cursor()
         # check if email is registered
         if cursor.execute("SELECT password FROM Users WHERE email = '{0}'".format(email)):
              data = cursor.fetchall()
              pwd = str(data[0][0] )
              if flask.request.form['password'] == pwd: # successful login
                   user = User()
                   user.id = email
                   flask_login.login_user(user)
                   return flask.redirect(flask.url_for('protected'))
              else: # failed login
                   return render_template("unauth.html")
              
@app.route("/logout")
def logout():
     flask_login.logout_user()
     return render_template('welcome.html', message='Logged Out')

@login_manager.unauthorized_handler
def unauthorized_handler():
     return render_template('unauth.html')



# sign up page - on success move to hello, on failure show error
@app.route("/signup", methods=['GET'])
def signup():
    return render_template("signup.html", supress=True)
@app.route("/signup", methods=['POST'])
def signup_user():
    # see if email is unique/valid to sign up
    try:
        email=request.form.get('email')
        password=request.form.get('password')
    except:
        print("couldn't find all tokens")
        return flask.redirect(flask.url_for('signup'))
    cursor = conn.cursor()
    test = isEmailUnique(email)
    if test: # successfull sign up
         dob=request.form.get('dob')
         hometown=request.form.get('hometown')
         gender=request.form.get('gender')
         fname=request.form.get('firstname')
         lname=request.form.get('lastname')
         print(cursor.execute("INSERT INTO Users (email, password, dob, hometown, gender, fname, lname) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}')".format(email, password, dob, hometown, gender, fname, lname)))
         conn.commit()
         # user automatically is logged in
         user = User()
         user.id = email
         flask_login.login_user(user)
         return render_template('hello.html', name=email, message='Account Created!')
    else: # unsuccessful sign up
         print("couldn't find all tokens")
         return render_template("unauth.html")
    
def getUsersPhotos(uid):
     cursor = conn.cursor()
     cursor.execute("SELECT imgdata, picture_id, caption, album_id FROM Pictures WHERE user_id = '{0}'".format(uid))
     return cursor.fetchall() 

def getUserIdFromEmail(email):
     cursor = conn.cursor()
     cursor.execute("SELECT user_id FROM Users WHERE email = '{0}'".format(email))
     return cursor.fetchone()[0]

def getUserEmailFromId(uid):
     cursor = conn.cursor()
     cursor.execute("SELECT email FROM Users WHERE user_id = '{0}'".format(uid))
     return cursor.fetchone()[0]

def isEmailUnique(email):
     cursor = conn.cursor()
     if cursor.execute("SELECT email FROM Users WHERE email = '{0}'".format(email)):
          return False # email already has an account
     else:
          return True # email is unique

# helper functions     
def getUsersAlbums(uid):
     cursor = conn.cursor()
     cursor.execute("SELECT Name FROM Albums WHERE user_id = '{0}'".format(uid))
     return cursor.fetchall()

def getAlbumIDFromName(Name):
     uid = getUserIdFromEmail(flask_login.current_user.id) 
     cursor = conn.cursor()
     cursor.execute("SELECT album_id FROM Albums WHERE Name = '{0}' AND user_id = '{1}'".format(Name, uid))
     return cursor.fetchone()

def getUsersFriendsID(uid):
     cursor = conn.cursor()
     cursor.execute("SELECT UID2 FROM Friendship WHERE UID1 = '{0}'".format(uid))
     l = cursor.fetchall()
     return getUsersFriends(l)

def getUsersFriends(l):
    friends = []
    for id in l:
         for x in id:
            friends.append(getUserEmailFromId(x))
    return friends

def getUsersRecFriends(uid):
    recfriends = getUsersFriendsID(uid)
    total_recommendation = []
    for femail in recfriends:
        get_fid = getUserIdFromEmail(femail)
        recommend = getUsersFriendsID(get_fid)   
        total_recommendation.append(recommend)
    return getUsersRecTotal(total_recommendation, uid)

def getUsersRecTotal(l, uid):
     recfriends = []
     uemail = getUserEmailFromId(uid)
     for rec in l:
          for x in rec:
            if x in recfriends:
                 None
            elif x in getUsersFriendsID(uid):
                 None 
            elif x == uemail:
                 None
            else:
                recfriends.append(x)
     return recfriends 

def getPhotosInAlbum(Name):
     album_id = getAlbumIDFromName(Name)[0]
     cursor = conn.cursor()
     cursor.execute("SELECT imgdata, picture_id, caption FROM Pictures WHERE album_id = '{0}'".format(album_id))
     return cursor.fetchall()

def getTagID(Tag):
     cursor = conn.cursor()
     cursor.execute("SELECT tag_id FROM Tags WHERE name = '{0}'".format(Tag))
     l = cursor.fetchall()
     return l[0][0] 
     
def getPhotosComments(Name):
     photos = getPhotosInAlbum(Name)
     for photo in photos:
        picture_id = photo[1]
        cursor = conn.cursor()
        cursor.execute("SELECT text FROM Comments WHERE picture_id = '{0}'".format(picture_id))
     return cursor.fetchall()

def getPhotosTags(Name):
     photos = getPhotosInAlbum(Name)
     for photo in photos:
        picture_id = photo[1]
        cursor = conn.cursor()
        cursor.execute("SELECT tag_id FROM Tagged WHERE picture_id = '{0}'".format(picture_id))
        tag_ids = cursor.fetchall()
        if tag_ids == None:
             return None
        tagids_list =[]
        for tag_id in tag_ids:
             tag_id = tag_id[0]
             print("pls", tag_id)
             tagids_list.append(tag_id)
        return getTagName(tagids_list)
     
def getTagName(tagids_list):
     tags_list=[]
     for tag_id in tagids_list:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM Tags WHERE tag_id = '{0}'".format(tag_id))
        tag = cursor.fetchone()[0]
        tags_list.append(tag)
     return tags_list


def getPhotoAlbName(picture_id):
     uid = getUserIdFromEmail(flask_login.current_user.id) 
     print("pictureid is", picture_id)
     cursor = conn.cursor()
     cursor.execute("SELECT album_id FROM Pictures WHERE picture_id = '{0}'".format(picture_id))
     l = cursor.fetchone()[0]
     return getAlbNameFromID(l)

def getAlbNameFromID(l):
     cursor = conn.cursor()
     cursor.execute("SELECT Name FROM Albums WHERE album_id = '{0}'".format(l))
     x = cursor.fetchone()[0]
     return x

def getPhotoComments(picture_id):
     cursor = conn.cursor()
     cursor.execute("SELECT text FROM Comments WHERE picture_id = {0}'".format(picture_id))
     return cursor.fetchall()

def isTagUnique(Tag):
     cursor = conn.cursor()
     if cursor.execute("SELECT tag_id FROM Tags WHERE name = '{0}'".format(Tag)):
          return False # email already has an account
     else:
          return True # email is unique

# unauthorized page - only used for a failed login/signup
@app.route("/unauth", methods=['GET'])
def unauth():
    return render_template("unauth.html")


# main profile homepage for logged in users
@app.route("/hello", methods=['GET'])
@flask_login.login_required
def protected():
    uid = getUserIdFromEmail(flask_login.current_user.id)
    return render_template("hello.html", name=flask_login.current_user.id, 
                           albums=getUsersAlbums(uid), friends=getUsersFriendsID(uid), recfriends=getUsersRecFriends(uid) ,message="Here's your profile")

# opens a users selected albums page from their list of albums
@app.route("/created_albs/<Name>")
@flask_login.login_required
def created_albs(Name):
    uid = getUserIdFromEmail(flask_login.current_user.id)
    Name = Name[2:-3]
    photos = getPhotosInAlbum(Name)
    for photo in photos:
        print("ID IS", photo[1])
    return render_template("created_albs.html", Name=Name, photos=photos, Tags=getPhotosTags(Name), Comments=getPhotosComments(Name), base64=base64)

# adding a tag to a picture
@app.route("/addTag/<picture_id>", methods=['GET', 'POST'])
@flask_login.login_required
def addTag(picture_id):
    if request.method == 'POST':
         Tag = request.form.get('Tag')
         if isTagUnique(Tag): # tag_id not created
              cursor = conn.cursor()
              cursor.execute("INSERT INTO Tags (name) VALUES ('{0}')".format(Tag))
              conn.commit()
              tag_id = getTagID(Tag)
              cursor = conn.cursor()
              cursor.execute("INSERT INTO Tagged (picture_id, tag_id) VALUES ('{0}', '{1}')".format(picture_id, tag_id))
              conn.commit()
              album_name = getPhotoAlbName(picture_id)
              return render_template("created_albs.html", Name=album_name, photos=getPhotosInAlbum(album_name), Tags=getPhotosTags(album_name), Comments=getPhotosComments(album_name), base64=base64)
         else: # tag_id created
              print("Tag is , ", Tag)
              tag_id = getTagID(Tag)
              cursor = conn.cursor()
              cursor.execute("INSERT INTO Tagged (picture_id, tag_id) VALUES ('{0}', '{1}')".format(picture_id, tag_id))
              conn.commit()
              album_name = getPhotoAlbName(picture_id)
              return render_template("created_albs.html", Name=album_name, photos=getPhotosInAlbum(album_name), Tags=getPhotosTags(album_name), Comments=getPhotosComments(album_name), base64=base64)
    else:
         uid = getUserIdFromEmail(flask_login.current_user.id)
         return render_template("addTag.html", picture_id=picture_id)  

# viewing a friends prfile
@app.route('/friend_profile/<Friend>')
@flask_login.login_required
def friend_profile(Friend):
     uid = getUserIdFromEmail(flask_login.current_user.id)
     photos = getUsersPhotos(getUserIdFromEmail(Friend))
     return render_template("friend_profile.html", Friend=Friend, photos=photos, base64=base64)


# allowing photo types to be uploaded
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


# uploading a new photo to a users account
@app.route("/upload", methods=['GET', 'POST'])
@flask_login.login_required
def upload():
    if request.method == 'POST':
        uid = getUserIdFromEmail(flask_login.current_user.id)
        imgfile = request.files['photo']
        caption = request.form.get('caption')
        photo_data = imgfile.read()
        Name = request.form.get('Name')
        album_id = getAlbumIDFromName(Name)
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO Pictures (user_id, caption, imgdata, album_id) VALUES (%s, %s, %s, %s)''',(uid, caption, photo_data, album_id[0]))
        conn.commit()
        return render_template('hello.html', name=flask_login.current_user.id, message='Photo uploaded!', albums=getUsersAlbums(uid), photos=getUsersPhotos(uid), friends=getUsersFriendsID(uid), recfriends=getUsersRecFriends(uid), base64=base64)
    else:    
        uid = getUserIdFromEmail(flask_login.current_user.id)
        return render_template("upload.html", albums = getUsersAlbums(uid))

# creating a new album
@app.route("/album", methods=['GET', 'POST'])
@flask_login.login_required
def album():
     if request.method == 'POST':
          Name = request.form.get('Name')
          uid = getUserIdFromEmail(flask_login.current_user.id)
          cursor = conn.cursor()
          cursor.execute("INSERT INTO Albums (Name, user_id) VALUES ('{0}', '{1}')".format(Name, uid))
          conn.commit()
          return render_template('hello.html', name=flask_login.current_user.id, message='Album created!', albums=getUsersAlbums(uid), friends=getUsersFriendsID(uid), recfriends=getUsersRecFriends(uid))
     else:
          return render_template("album.html")

# adding a new friend by their email address  
@app.route("/addFriend", methods=['GET','POST'])
@flask_login.login_required
def addFriend():
     if request.method == 'POST':
          femail = request.form.get('femail')
          if isEmailUnique(femail): # email is not registered with a current user
               return render_template("noAccount.html")
          else: # email is registered with a current user
            fid = getUserIdFromEmail(femail)
            uid = getUserIdFromEmail(flask_login.current_user.id)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO Friendship (UID1, UID2) VALUES ('{0}', '{1}')".format(uid, fid))
            conn.commit()
            return render_template('hello.html', name=flask_login.current_user.id, message='Friend Added!', albums=getUsersAlbums(uid), friends=getUsersFriendsID(uid), recfriends=getUsersRecFriends(uid))
     else:
          return render_template("addFriend.html")

# error page for an add friend request not valid  
@app.route("/noAccount")
def noAccount():
     return render_template("noAccount.html")

#gives the top 3 tags from everyone using the application
@app.route("/topTags")
def topTags():
     cursor = conn.cursor()
     cursor.execute("SELECT name, COUNT(*) FROM Tags NATURAL JOIN Tagged GROUP BY name ORDER BY COUNT(*) DESC LIMIT 3")
     data = cursor.fetchall()
     return render_template("topTags.html", data=data)


if __name__ == "__main__":
	#this is invoked when in the shell  you run
	#$ python app.py
	app.run(port=9000, debug=True)