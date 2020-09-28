import datetime
import sqlalchemy
from sqlalchemy import orm
import data.users
import data.replies
from .db_session import SqlAlchemyBase


class Articles(SqlAlchemyBase):
    __tablename__ = 'articles' 
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, nullable=False)
    title = sqlalchemy.Column(sqlalchemy.String(150), nullable=False, unique=False)
    content = sqlalchemy.Column(sqlalchemy.String(2500), nullable=False, unique=False)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, 
                                sqlalchemy.ForeignKey("users.id"))
    generated_id = sqlalchemy.Column(sqlalchemy.String(8), nullable=False, unique=True)
    user = orm.relation('User')
    def __str__(self):
        return self.title