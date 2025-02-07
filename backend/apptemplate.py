import os
from flask import request, render_template, jsonify
from config import app, SALT
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from project.models import db, User, AudioRecording
from flask_jwt_extended import (
    create_access_token,
    JWTManager,
    jwt_required,
    get_jwt_identity,
)
from flask_cors import CORS
import hashlib

JWT = JWTManager(app)
ERROR = "error has occured"
CORS(app)

# Endpoint for homepage
@app.route("/")
@jwt_required()
def home():
    current_username = get_jwt_identity()["username"]

    try:
        user = User.query.filter_by(username=current_username).first()
        serialized_user = user.as_dict()

        response = jsonify(serialized_user)
        response.status_code = 200
    except Exception:
        response = jsonify({"status": ERROR})
        response.status_code = 500

    return response


# Endpoint for login page
@app.route("/login")
def login():
    return render_template("login.html")


# Endpoint for register page
@app.route("/register")
def register():
    return render_template("register.html")


# Endpoint to retrieve all the recordings
@app.route("/api/recordings")
def get_all_recordings():
    recordings_list = list(AudioRecording.query.all())

    # Serializing the recordings in the list
    recordings_serialzied = [recording.as_dict() for recording in recordings_list]

    data = {"recordings": recordings_serialzied}

    response = jsonify(data)
    response.status_code = 200

    return response


# Endpoint to retrieve the current logged in user
@app.route("/api/current_user", methods=["GET"])
@jwt_required()
def current_user():
    current_username = get_jwt_identity()["username"]

    try:
        user = User.query.filter_by(username=current_username).first()
        serialized_user = user.as_dict()

        response = jsonify(serialized_user)
        response.status_code = 200
    except Exception:
        response = jsonify({"status": ERROR})
        response.status_code = 500

    return response


# Endpoint to login user
@app.route("/api/login", methods=["POST"])
def login_auth():
    data = request.get_json()
    print(data)
    if data:
        username = data["username"]
        password = data["password"]

        password_salt = password + SALT
        password_hash = hashlib.sha256(password_salt.encode("utf-8")).hexdigest()

        user = User.query.filter_by(username=username, password=password_hash).first()

        if user:
            access_token = create_access_token(identity={"username": username})
            response = jsonify(
                {"token": access_token, "status": "Succesfully logged in user"}
            )
            response.status_code = 200
        else:
            response = jsonify({"status": "Incorrect username or password"})
            response.status_code = 200
    else:
        response = jsonify({"status": ERROR})
        response.status_code = 500

    return response


# Endpoint to register a new user
@app.route("/api/register", methods=["POST"])
def register_auth():
    data = request.get_json()
    print(data)
    if data:
        first_name = data["first_name"]
        last_name = data["last_name"]
        username = data["username"]
        password = data["password"]
        email_address = data["email_address"]

        password_salt = password + SALT
        password_hash = hashlib.sha256(password_salt.encode("utf-8")).hexdigest()

        # Duplicate user
        user = User.query.filter_by(username=username).first()

        if user:
            response = jsonify(
                {"status": "there is already a user with the same username"}
            )
            response.status_code = 200
        else:
            new_user = User(
                username=username,
                first_name=first_name,
                last_name=last_name,
                password=password_hash,
                email_address=email_address,
            )
            db.session.add(new_user)
            db.session.commit()

            access_token = create_access_token(identity={"username": username})

            response = jsonify(
                {"status": "Succesfully created user", "token": access_token}
            )
            response.status_code = 200

    else:
        response = jsonify({"status": ERROR})
        response.status_code = 500

    return response


# attempt to have 1 route load all pages of forum that you can scroll though
#page for any user to see all posts
@app.route("/api/forum" + str(forum_page), methods=["POST"])
def forum():
    #first page loaded forum page = 1
    #get all post
    posts = Post.as_dict()
    #how many pages there should be 10 is the current number of post per page randomly decided can be changed
    forum_total = len(posts)/ 10 + len(posts) % 10 
    #somehow display 10 post per page in reverse order since newer post have higher number based on id send it to frontend


#unique page of player's songs
 @app.route("/api/mysongs" + str(song_page), methods=["POST"])
def mysongs():
    #get uid id based on username
    data = request.get_json()
    if data:
        username = data["username"]
        songs = AudioRecording.query.filter(id = uid)
        #first song_page = 1;
        #how many pages there should be
        song_total = len(song)/ 10 + len(song) % 10 
        #somehow display 10 post per page in reverse order since newer post have higher number based on id   


@app.route("/api/newpost" , methods=["POST"])
def newpost():
    data = request.get_json()
    print(data)
    if data:
        username = data["username"]
        user = User.query.filter_by(username=username, password=password_hash).first()
        #get uid from user or db
        #audio id
        uid 
        aid
        #get the content from page
        content
        new_post = Post(
            user_id = uid,
            audio_id = aid,
            text = content,
            #date
        )
        db.session.add(new_post)
        db.session.commit()

@app.route("/api/post" + str(pid), methods=["POST"])
def post():
        #should be able to view the post all the comments of the post and then post a comment 
        #get post_id from last page
        pid
        post = Post.query.filter(id = pid)
        comments = Comment.query.filter(post_id = pid)
        #get the text of the comment from page
        comm
        new_comment = Comment(
            post_id = pid
            text = comm
        )


if __name__ == "__main__":
    app.run(debug=True)
