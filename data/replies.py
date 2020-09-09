import datetime
import sqlalchemy
from sqlalchemy import orm
import data.users
import data.questions
from .db_session import SqlAlchemyBase


class Replies(SqlAlchemyBase):
    __tablename__ = 'replies' 
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, nullable=False)
    text = sqlalchemy.Column(sqlalchemy.String(50), nullable=False, unique=False)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, 
                                sqlalchemy.ForeignKey("users.id"))
    question_id = sqlalchemy.Column(sqlalchemy.Integer, 
                                sqlalchemy.ForeignKey("questions.id"))
    user = orm.relation('User')
    def __str__(self):
        return self.question_id