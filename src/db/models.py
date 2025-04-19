import uuid
from datetime import datetime

import sqlalchemy.dialects.postgresql as pg
from sqlmodel import SQLModel, Field, Column


class User(SQLModel, table=True):
    """User entity"""
    __tablename__ = 'tb_users'

    uid: uuid.UUID = Field(sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4))
    first_name: str = Field(sa_column=Column(pg.VARCHAR, nullable=False))
    last_name: str = Field(sa_column=Column(pg.VARCHAR, nullable=False))
    username: str = Field(sa_column=Column(pg.VARCHAR, nullable=False, unique=True))
    email: str = Field(sa_column=Column(pg.VARCHAR, nullable=False, unique=True))
    password: str = Field(exclude=True, nullable=False)
    is_verified: bool = Field(default=False)
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))

    def __repr__(self):
        return f'<User {self.username}>'
