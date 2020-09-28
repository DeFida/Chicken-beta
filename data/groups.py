import datetime
import sqlalchemy
from sqlalchemy import orm
import data.users
from .db_session import SqlAlchemyBase


class Groups(SqlAlchemyBase):
    __tablename__ = 'groups' 
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, nullable=False)
    name = sqlalchemy.Column(sqlalchemy.String(150), nullable=False, unique=False)
    members_count = sqlalchemy.Column(sqlalchemy.Integer, nullable=False, unique=False)
    members = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    team_logo = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    generated_id = sqlalchemy.Column(sqlalchemy.String(8), nullable=False, unique=True)
    description = sqlalchemy.Column(sqlalchemy.String(50))
    user_id = sqlalchemy.Column(sqlalchemy.Integer, 
                                sqlalchemy.ForeignKey("users.id"))
    user = orm.relation('User')
    def __str__(self):
        return self.name