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


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


@app.route("/questions/", methods=["GET"])
def index():
    return render_template("base.html", side_bar_title="Сұрақтарым")
 

if __name__ == "__main__":
    app.run(debug=True)