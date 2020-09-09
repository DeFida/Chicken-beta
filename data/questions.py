import datetime
import sqlalchemy
from sqlalchemy import orm
import data.users
import data.replies
from .db_session import SqlAlchemyBase


class Questions(SqlAlchemyBase):
    __tablename__ = 'questions' 
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, nullable=False)
    title = sqlalchemy.Column(sqlalchemy.String(50), nullable=False, unique=False)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, 
                                sqlalchemy.ForeignKey("users.id"))
    reply = sqlalchemy.Column(sqlalchemy.Integer, 
                                sqlalchemy.ForeignKey("replies.id"))
    name_img = sqlalchemy.Column(sqlalchemy.String(50), nullable=False, unique=False)
    tags = sqlalchemy.Column(sqlalchemy.String(30))
    user = orm.relation('User')
    def __str__(self):
        return self.title