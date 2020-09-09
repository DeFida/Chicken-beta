import datetime
import sqlalchemy
from sqlalchemy import orm
import data.users
from .db_session import SqlAlchemyBase


class Replies(SqlAlchemyBase):
    __tablename__ = 'replies' 
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, nullable=False)
    name = sqlalchemy.Column(sqlalchemy.String(50), nullable=False, unique=False)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, 
                                sqlalchemy.ForeignKey("users.id"))
    owner = sqlalchemy.Column(sqlalchemy.String)
    phone_number = sqlalchemy.Column(sqlalchemy.Integer, unique=True)
    service_type = sqlalchemy.Column(sqlalchemy.String)
    user = orm.relation('User')
    is_open = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True)
    def __str__(self):
        return self.name