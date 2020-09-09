# Dastan
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, abort
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
import stripe
from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache
from flask_login import LoginManager, logout_user, current_user, login_user, login_required
from datetime import datetime, timedelta
from markupsafe import escape
from passlib.hash import sha256_crypt
# from forms import RegisterForm, LoginForm, AddServices, PublishServicePost
# from data import db_session
# from data.users import User
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
# db_session.global_init("db/data.sqlite")
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = "strong"
service_ch = None


# print(stripe.Customer.retrieve('sub_HcgoijxNFgxdBz'))
class OurModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

class OurAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.admin

admin = Admin(app, index_view=OurAdminIndexView(), name="Chicken")
# admin.add_view(OurModelView(User, db_session.create_session()))
# admin.add_view(OurModelView(Services, db_session.create_session()))



@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


# @app.route("/hot/", methods=['GET', 'POST'])
# def services():
#     return render_template("services.html")


# @app.route('/signin/', methods=['POST', 'GET'])
# def signin():
#     form = LoginForm()
#     if form.validate_on_submit():
#         session = db_session.create_session()
#         user = session.query(User).filter(User.username == form.username.data).first()
#         if user and check_password_hash(user.password, form.password.data):
#             print("name - " + user.name)
#             login_user(user, remember=form.remember_me.data)
#             return redirect("/")
#         return render_template('signin.html',
#                                message="Неправильный логин или пароль",
#                                form=form, alert_var=True)
#     return render_template('signin.html', form=form, alert_var=False)

 
# @app.route("/signup/", methods=['POST', 'GET'])
# def signup():
#     form = RegisterForm()
#     if form.validate_on_submit():
#         session = db_session.create_session()
#         user = User(
#             name=form.name.data,
#             email=form.email.data,
#             username=form.username.data,
#             password=generate_password_hash(form.password.data)
#         )
#         session.add(user)
#         session.commit()
#         return redirect('/signin')
#     return render_template('signup.html', form=form, alert=False)


# @app.route("/logout/")
# def logout():
#     logout_user()
#     return redirect("/")


# @app.route("/about/")
# def about():
#     return render_template("about.html")


# @app.route("/search", methods=['GET', 'POST'])
# def search():
#     result = list()
#     session = db_session.create_session()
#     q = request.args.get('q').lower()
#     s = request.args.get('s')
#     print(q, s)
#     query_item = str()
#     if s == 'products':
#         query_item = Products
#     elif s == 'services':
#         query_item = Services
#     elif s == 'businessmen':
#         query_item = User
#     search_items = session.query(query_item).all()
#     for item in search_items:
#         if q in (item.name).lower() or q in (item.address).lower():
#             result.append(item)
#     if len(result) == 0:
#         message = "Ничего не найдено по вашему запросу: " + q
#         return render_template("search.html", spisok_servicov=message)
#     return render_template("search.html", spisok_servicov=result)
    

if __name__ == "__main__":
    app.run(debug=True)