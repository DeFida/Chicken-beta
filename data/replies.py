import datetime
import sqlalchemy
from sqlalchemy import orm
import data.users
from .db_session import SqlAlchemyBase


class Replies(SqlAlchemyBase):
    __tablename__ = 'replies' 
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, nullable=False)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, 
                                sqlalchemy.ForeignKey("users.id"))
    text = sqlalchemy.Column(sqlalchemy.String)
    user = orm.relation('User')
    def __str__(self):
        return self.name