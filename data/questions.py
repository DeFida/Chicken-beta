import datetime
import sqlalchemy
from sqlalchemy import orm
import data.users
import data.replies
from .db_session import SqlAlchemyBase


class Questions(SqlAlchemyBase):
    __tablename__ = 'questions' 
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, nullable=False)
    name = sqlalchemy.Column(sqlalchemy.String(50), nullable=False, unique=False)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, 
                                sqlalchemy.ForeignKey("users.id"))
    serv_id = sqlalchemy.Column(sqlalchemy.Integer, 
                                sqlalchemy.ForeignKey("services.id"))
    name_img = sqlalchemy.Column(sqlalchemy.String(50), nullable=False, unique=False)
    owner = sqlalchemy.Column(sqlalchemy.String)
    phone_number = sqlalchemy.Column(sqlalchemy.Integer, unique=True)
    tags = sqlalchemy.Column(sqlalchemy.String(30))
    description = sqlalchemy.Column(sqlalchemy.String(180)) 
    user = orm.relation('User')

    def __str__(self):
        return self.name