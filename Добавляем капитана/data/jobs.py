import datetime
import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Jobs(SqlAlchemyBase):
    __tablename__ = 'jobs'

    id = sqlalchemy.Column(sqlalchemy.Integer, 
                           primary_key=True, autoincrement=True)

    team_leader = sqlalchemy.Column(sqlalchemy.Integer, 
                                sqlalchemy.ForeignKey("users.id"))

    job = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    collaborators = sqlalchemy.Column(sqlalchemy.String)

    work_size = sqlalchemy.Column(sqlalchemy.Integer)

    start_date = sqlalchemy.Column(sqlalchemy.String)

    end_date = sqlalchemy.Column(sqlalchemy.String)
    
    is_finished = sqlalchemy.Column(sqlalchemy.Boolean, default=True)

    user = orm.relationship('User')
    