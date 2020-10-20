# Dastan
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, abort
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_caching import Cache
from flask_login import LoginManager, logout_user, current_user, login_user, login_required
from werkzeug.utils import secure_filename
from datetime import timedelta
from string import ascii_lowercase, digits
from data import db_session
from data.users import User
from data.questions import Questions
from data.replies import Replies
from data.groups import Groups
from data.articles import Articles
from werkzeug.security import generate_password_hash, check_password_hash
from random import choice
import os


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
    if model == "Groups":
        var1 = session.query(Groups).filter(Groups.generated_id == generated_id).first()
    if model == "Replies":
        var1 = session.query(Questions).filter(Questions.generated_id == generated_id).first()
    if model == "Articles":
        var1 = session.query(Articles).filter(Articles.generated_id == generated_id).first()
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
    session = db_session.create_session()
    questions = session.query(Questions).filter().all()
    actual_q = questions[0:6]
    return render_template("index.html", actual_q=actual_q)


@app.route("/sign_up/", methods=["POST", "GET"])
def sign_up():
    username = request.args.get('username').lower()
    email = request.args.get('email').lower()
    password = request.args.get('password').lower()
    session = db_session.create_session()
    if session.query(User).filter(User.username == username).first():
        return jsonify(error='Сіз жазған логин тіркелген')
    if session.query(User).filter(User.email == email).first():
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
    if user and not check_password_hash(user.password, password):
        return jsonify(error="Құпиясөз қате")
    if user and check_password_hash(user.password, password):
        print("username - " + user.username)
        login_user(user, remember=True)
        return jsonify(error="No error")


@app.route("/questions/", methods=["GET"])
def categories():
    session = db_session.create_session()
    q = session.query(Questions).all()[::-1]
    groups = session.query(Groups).all()[::-1]
    articles = session.query(Articles).all()[::-1]
    my_groups = []
    my_articles = []
    for group in groups:
        if current_user.username in group.members:
            my_groups.append(group)
    for article in articles[:6]:
        my_articles.append(article)
    return render_template("categories.html", questions=q, my_groups=my_groups, articles=my_articles)

@app.route("/all_articles/", methods=["GET"])
def all_articles():
    session = db_session.create_session()
    groups = session.query(Groups).all()[::-1]
    articles = session.query(Articles).all()[::-1]
    my_groups = []
    my_articles = []
    for group in groups:
        if current_user.username in group.members:
            my_groups.append(group)
    for article in articles[:6]:
        my_articles.append(article)
    return render_template("articles_all.html", my_groups=my_groups, my_articles=my_articles, articles=articles)


@app.route("/questions/<string:id>", methods=["GET"])
def question(id):
    session = db_session.create_session()
    q = session.query(Questions).filter(Questions.generated_id == id).first()
    reps = session.query(Replies).filter(Replies.question_id == id).all()[::-1]
    return render_template("question.html", q=q, reps=reps)

    


@app.route("/groups/<string:id>", methods=["GET"])
def groups(id):
    session = db_session.create_session()
    g = session.query(Groups).filter(Groups.generated_id == id).first()
    members = g.members.split()
    return render_template("group.html", g=g, members=members)


@app.route("/articles/<string:id>", methods=["GET"])
def articles(id):
    session = db_session.create_session()
    a = session.query(Articles).filter(Articles.generated_id == id).first()
    return render_template("article.html", a=a)


@app.route("/user_profile/", methods=["GET"])
def user_profile():
    session = db_session.create_session()
    questions = session.query(Questions).filter(Questions.user_id == current_user.id).all()[:]
    replies = session.query(Replies).filter(Replies.user_id == current_user.id).all()
    print(replies)
    return render_template("profile.html", questions=questions, replies=replies)


@app.route("/new_group/", methods=["GET", "POST"])
def new_group():
    return render_template("add_group.html")

@app.route("/write_article/", methods=["GET", "POST"])
def write_article():
    return render_template("articles.html")

@app.route("/add_group/", methods=["GET", "POST"])
@login_required
def add_group():
    group_name = request.args.get('group_name')
    description = request.args.get('description')
    members = request.args.get('members')
    generated_id = id_generator("Groups")
    session = db_session.create_session()
    print(group_name, description, generated_id, current_user.id, members)
    g = Groups(
        name=group_name,
        description=description,
        generated_id=generated_id,
        user_id=current_user.id,
        members_count=1,
        members=current_user.username + members
    )
    session.add(g)
    session.commit()
    path = mkdir("groups", generated_id)
    print(path)
    if request.files:
        img = request.files["avatar"]
        print(img.filename)
        img.save(os.path.join(path, img.filename))
    return jsonify({"generated_id": generated_id})


@app.route("/add_article/", methods=["GET", "POST"])
@login_required
def add_article():
    article_title = request.args.get('article_title')
    content = request.args.get('content')
    generated_id = id_generator("Articles")
    session = db_session.create_session()
    print(article_title, content, generated_id, current_user.id)
    a = Articles(
        title=article_title,
        content=content,
        generated_id=generated_id,
        user_id=current_user.id,
    )
    session.add(a)
    session.commit()
    path = mkdir("articles", generated_id)
    print(path)
    
    return jsonify({"generated_id": generated_id})

@app.route("/members", methods=["POST", "GET"])
def members():
    username = request.args.get('username')
    session = db_session.create_session()
    member = session.query(User).all()[:]
    list_temprary = []
    for i in member:
        if i.username != current_user.username and username in i.username:
            list_temprary.append(i)
    member = list_temprary[:]
    ls = {}
    for i in range(len(member)):
        ls[i] = {'username': member[i].username, 'id': member[i].generated_id}
    if member == None or username == '':
        username = '-1-1-2-2-None-2-2-1-1-'
        logopath = None
    logopath = '../static/images/unknownperson.png'
    return jsonify({'list': ls, 'username': username})

@app.route("/new_qa/", methods=["POST"])
@login_required
def new_qa():
    question__title = request.form['val1']
    question__main_text = request.form['val2']
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
    if 'files[]' not in request.files:
        print("nofile")
        return jsonify({"generated_id": generated_id})
    files = request.files.getlist('files[]')
    img_count = 0
    path = mkdir("questions", generated_id)
    print(path)
    for file_ in files:
        extension = file_.filename.split('.')[-1]
        if file_ and allowed_file(file_.filename):
            filename = secure_filename(file_.filename)
            file_.save(os.path.join(path, filename))
            img_count += 1
            os.rename(path + '\\' + filename, path + '\\' + str(img_count) + '.' + extension)

    return jsonify({"generated_id": generated_id})


@app.route("/reply/", methods=["POST", "GET"])
@login_required
def reply():
    r_content = request.form['val_textarea']
    q_id = request.form['question_id']
    generated_id = id_generator("Replies")
    session = db_session.create_session()
    r = Replies(
        text=r_content,
        question_id=q_id,
        generated_id=generated_id,
        user_id=current_user.id
    )
    q_rep_num = session.query(Questions).filter(Questions.generated_id == q_id).first()
    q_rep_num.rep_num += 1
    rep_num = q_rep_num.rep_num
    session.add(r)
    session.commit()
    print(r_content, q_id, generated_id)
    return jsonify({"generated_id": generated_id, "rep_num": rep_num})

if __name__ == "__main__":
    app.run(debug=True)