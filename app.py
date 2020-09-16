# Dastan
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, abort
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache
from flask_login import LoginManager, logout_user, current_user, login_user, login_required
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
from string import ascii_lowercase, digits
from passlib.hash import sha256_crypt
# from forms import RegisterForm, LoginForm, AddServices, PublishServicePost
from data import db_session
from data.users import User
from data.questions import Questions
from data.replies import Replies
from werkzeug.security import generate_password_hash, check_password_hash
from random import choice
import datetime
import os
from sqlalchemy import delete, update


app = Flask(__name__)
cache = Cache(config={'CACHE_TYPE': 'simple'})
cache.init_app(app)
app.secret_key = b'iw7d/546adit&#'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['REMEMBER_COOKIE_DURATION'] = timedelta(seconds=20)
db_session.global_init("db/data.sqlite")
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = "strong"
generator_ch = ascii_lowercase + digits
service_ch = None


class OurModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

class OurAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.admin

admin = Admin(app, index_view=OurAdminIndexView(), name="Chicken")
admin.add_view(OurModelView(User, db_session.create_session()))
admin.add_view(OurModelView(Questions, db_session.create_session()))
admin.add_view(OurModelView(Replies, db_session.create_session()))


def id_generator(model):
    global generator_ch
    generated_id = str()
    session = db_session.create_session()
    if model == "User":
        var1 = session.query(User).filter(User.generated_id == generated_id).first()
    if model == "Questions":
        var1 = session.query(Questions).filter(Questions.generated_id == generated_id).first()
    for i in range(8):
        generated_id += choice(generator_ch)
    while var1  != None:
        for i in range(8):
            generated_id += choice(generator_ch)
    return generated_id

# 'users', User, username, 'username'
def mkdir(dir_img, generated_id):
    parent_dir = r"static\images\{}".format(dir_img)
    directory = str(generated_id)
    path = os.path.join(parent_dir, directory)

    try:
        os.mkdir(path)
        print("folder created - " + path)
        return path
    except FileExistsError:
        pass


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg' ,'jfif', 'bmp'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


@app.route("/logout/")
def logout():
    logout_user()
    return redirect("/")


@app.route("/", methods=["GET", "POST"])
def main():
    return render_template("index.html")


@app.route("/sign_up/", methods=["POST", "GET"])
def sign_up():
    username = request.args.get('username').lower()
    email = request.args.get('email').lower()
    password = request.args.get('password').lower()
    session = db_session.create_session()
    if session.query(User).filter(User.username == username).first():
        return jsonify(error='Сіз жазған логин тіркелген')
    elif session.query(User).filter(User.email == email).first():
        return jsonify(error="Бұл e-mail тіркелген")
    generated_id=id_generator("User")
    user = User(
        email=email,
        username=username,
        password=generate_password_hash(password),
        generated_id=generated_id
    )
    session.add(user)
    session.commit()
    mkdir('users', generated_id)
    print('You were successfully logged in')
    return jsonify(error="No error")

@app.route("/sign_in/", methods=["POST", "GET"])
def sign_in():
    session = db_session.create_session()
    username = request.args.get('username_in').lower()
    password = request.args.get('password_in').lower()
    user = session.query(User).filter(User.username == username).first()
    if user == None:
        return jsonify(error="Есімнің дұрыстығына көз жеткізіңіз")
    elif user and not check_password_hash(user.password, password):
        return jsonify(error="Құпиясөз қате")
    elif user and check_password_hash(user.password, password):
        print("username - " + user.username)
        login_user(user, remember=True)
        return jsonify(error="No error")


@app.route("/questions/", methods=["GET"])
def categories():
    return render_template("categories.html")


@app.route("/user_profile/", methods=["GET"])
def user_profile():
    session = db_session.create_session()
    questions = session.query(Questions).filter(Questions.user_id == current_user.id).all()[:]
    replies = session.query(Replies).filter(Replies.user_id == current_user.id).all()[:]
    return render_template("profile.html", questions=questions)


@app.route("/new_qa/", methods=["POST"])
@login_required
def new_qa():
    question__title = request.form['question__title']
    question__main_text = request.form['question__main-text']
    generated_id = id_generator("Questions")
    session = db_session.create_session()
    q = Questions(
        title=question__title,
        content=question__main_text,
        generated_id=generated_id,
        user_id=current_user.id
    )
    session.add(q)
    session.commit()
    print(question__title, question__main_text, generated_id)
    path = mkdir("questions", generated_id)
    print(path)
    if 'files[]' not in request.files:
        print(404)
    files = request.files.getlist('files[]')
    img_count = 0
    for file_ in files:
        extension = file_.filename.split('.')[-1]
        if file_ and allowed_file(file_.filename):
            filename = secure_filename(file_.filename)
            file_.save(os.path.join(path, filename))
            img_count += 1
            os.rename(path + '\\' + filename, path + '\\' + str(img_count) + '.' + extension)

    return redirect('/questions')


if __name__ == "__main__":
    app.run(debug=True)