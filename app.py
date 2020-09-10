# Dastan
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, abort
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache
from flask_login import LoginManager, logout_user, current_user, login_user, login_required
from datetime import datetime, timedelta
from markupsafe import escape
from passlib.hash import sha256_crypt
# from forms import RegisterForm, LoginForm, AddServices, PublishServicePost
from data import db_session
from data.users import User
from data.questions import Questions
from data.replies import Replies
from werkzeug.security import generate_password_hash, check_password_hash
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


def mkdir(dir_img, ):
    parent_dir = r"static\img\{}".format(dir_img)
    directory = str(session.query(Services).filter(Services.address == service_ch.address).first().id)
    path = os.path.join(parent_dir, directory)

    try:
        os.mkdir(path)
    except FileExistsError:
        pass

    if request.files:
        img = request.files["file"]
        img.save(os.path.join(path, img.filename))


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
    if request.method == "POST":
        print(request.form['username'])
        username = request.form['username'].lower()
        email = request.form['email'].lower()
        password = request.form['password']
        session = db_session.create_session()
        username_err = str()
        if session.query(User).filter(User.username == username).first():
            username_err = "Бұл есім бос емес"
            flash(username_err)
            return render_template("index.html", username_err=username_err, sign_type="sign-up")
        if session.query(User).filter(User.email == email).first():
            email_err = "Бұл e-mail тіркелген"
            return render_template("index.html", email_err=email_err, sign_type="sign-up")
        user = User(
            email=email,
            username=username,
            password=generate_password_hash(password)
        )
        session.add(user)
        session.commit()
        flash('You were successfully logged in')
        return redirect('/sign-in/')
    if current_user.is_authenticated:
        return redirect("/home/")
    return redirect("/sign-in/")

@app.route("/<string:mode>/", methods=["GET", "POST"])
def index(mode):
    print(mode)
    mode_list = ['sign-in', 'sign-up', 'home']
    if mode == "home" and not current_user.is_authenticated:
        return redirect("/sign-in/")
    if mode in mode_list:
        return render_template("index.html", sign_type=mode)
    return '404'


@app.route("/login/", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username_err = str()
        password_err = str()
        session = db_session.create_session()
        username = request.form['username'].lower()
        password = request.form['password']
        user = session.query(User).filter(User.username == username).first()
        print(user)
        if user == None:
            username_err = "Есімнің дұрыстығына көз жеткізіңіз"
            flash(username_err)
            return render_template('index.html', sign_type="sign-in", username_err=username_err)
        if user and not check_password_hash(user.password, password):
            password_err = "Құпиясөз қате"
            flash(password_err)
            return render_template('index.html', sign_type="sign-in", password_err=password_err)
        if user and check_password_hash(user.password, password):
            print("username - " + user.username)
            login_user(user, remember=True)
            return redirect(url_for('main'))


@app.route("/questions/", methods=["GET"])
def questions():
    return render_template("questions.html", side_bar_title="Сұрақтарым")


@app.route("/new_qa/", methods=["POST"])
def add_qa():
    return render_template("new_qa.html")

@app.route("/signup/", methods=["POST"])
def signup():
    return render_template("signup.html")

if __name__ == "__main__":
    app.run(debug=True)