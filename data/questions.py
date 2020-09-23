import datetime
import sqlalchemy
from sqlalchemy import orm
import data.users
import data.replies
from .db_session import SqlAlchemyBase


class Questions(SqlAlchemyBase):
    __tablename__ = 'questions' 
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, nullable=False)
    title = sqlalchemy.Column(sqlalchemy.String(150), nullable=False, unique=False)
    content = sqlalchemy.Column(sqlalchemy.String(2500), nullable=False, unique=False)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, 
                                sqlalchemy.ForeignKey("users.id"))
    reply = sqlalchemy.Column(sqlalchemy.String(8), nullable=True)
    generated_id = sqlalchemy.Column(sqlalchemy.String(8), nullable=False, unique=True)
    rep_num = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    tags = sqlalchemy.Column(sqlalchemy.String(30))
    user = orm.relation('User')
    def __str__(self):
        return self.title