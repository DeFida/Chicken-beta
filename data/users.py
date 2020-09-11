import datetime
import sqlalchemy
from sqlalchemy import orm
from flask_login import UserMixin
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'users'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, nullable=False)
    generated_id = sqlalchemy.Column(sqlalchemy.String(8), unique=True)
    email = sqlalchemy.Column(sqlalchemy.String(255), nullable=False, unique=True)
    username = sqlalchemy.Column(sqlalchemy.String(35), nullable=False, unique=True)
    password = sqlalchemy.Column(sqlalchemy.String(255), nullable=False)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, 
                                     default=datetime.datetime.now)
    admin = sqlalchemy.Column(sqlalchemy.Boolean, nullable=False, default=False)
    rep = orm.relation("Replies", back_populates='user')
    qst = orm.relation("Questions", back_populates='user')

    def __repr__(self):
        return self.username

        