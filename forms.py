from flask_wtf import FlaskForm
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms.fields.html5 import EmailField
from wtforms.fields.simple import TextAreaField 
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from wtforms import StringField, SelectField, PasswordField, BooleanField, SubmitField, FileField, IntegerField
from data.__all_models import *
from data import db_session



class LoginForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField(validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')
    def validate_username(self, username):
        session = db_session.create_session()
        user = session.query(users.User).filter_by(username=username.data).first()
        if user == None:
            raise ValidationError("Никнейм '" + username.data + "' не существует")

    def validate_password(self, email):
        session = db_session.create_session()
        user = session.query(users.User).filter_by(username=username.data).first()

        if user and not check_password_hash(user.password, password.data):
            raise ValidationError('Неправильный пароль')


class RegisterForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    name = StringField('Имя пользователя', validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')
    def validate_username(self, username):
        session = db_session.create_session()
        user = session.query(users.User).filter_by(username=username.data).first()
        if user:
            raise ValidationError("Никнейм '" + username.data + "' уже занят. Выберите другой.")

    def validate_email(self, email):
        session = db_session.create_session()
        user = session.query(users.User).filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

class PublishServicePost(FlaskForm):
    title_of_post = StringField('Title', validators=[DataRequired()])
    content = StringField('Content', validators=[DataRequired()])
    submit = SubmitField('Publish')


class AddServices(FlaskForm):
    name = StringField('Название сервиса', validators=[DataRequired()])
    address = TextAreaField("Адрес", validators=[DataRequired()])
    phone_number = IntegerField("Телефонный номер", validators=[DataRequired()])
    submit = SubmitField('Отправить заявку')
    service = SelectField('service', choices=[('res', 'Рестораны'), ('cloth', 'Магазин одежды'),
                            ('foodShops', 'Продуктовые магазины'), ('tire', 'Шиномонтаж'),
                            ('vehicle_repairs', 'Станция технического обслуживания')])
                            
    search = StringField("Поиск")
