import sqlalchemy
from sqlalchemy import orm
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
    generated_id = sqlalchemy.Column(sqlalchemy.String(8), nullable=False, unique=True)
    votes = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    user = orm.relation('User')
    def __str__(self):
        return self.question_id