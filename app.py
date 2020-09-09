
from flask import Flask, render_template, redirect, request
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, logout_user, current_user, login_user, login_required


app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    render_template("index.html")


if __name__ == "__main__":
    app.run()

