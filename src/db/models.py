"""
Class responsible for table models (entities)
"""
import uuid
from datetime import datetime
from typing import List, Optional

import sqlalchemy.dialects.postgresql as pg
from sqlmodel import SQLModel, Field, Column, Relationship


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


class Category(SQLModel, table=True):
    """Embrapa Viticulture with main categories"""
    __tablename__ = 'tb_category'

    uid: uuid.UUID = Field(sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4))
    category: str = Field(sa_column=Column(pg.VARCHAR, nullable=False))
    subcategories: List['SubCategory'] = Relationship(back_populates='category',
                                                      sa_relationship_kwargs={'lazy': 'selectin'})
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))

    def __repr__(self):
        return f'<Category {self.category}>'


class SubCategory(SQLModel, table=True):
    """Embrapa Viticulture with subcategories"""
    __tablename__ = 'tb_subcategory'
    uid: uuid.UUID = Field(sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4))
    subcategory: str = Field(sa_column=Column(pg.VARCHAR, nullable=False))
    control: str = Field(sa_column=Column(pg.VARCHAR))
    product: str = Field(sa_column=Column(pg.VARCHAR))
    country: str = Field(sa_column=Column(pg.VARCHAR))
    qty_product: int = Field(sa_column=Column(pg.FLOAT))
    vl_product: float = Field(sa_column=Column(pg.FLOAT))
    year: int = Field(sa_column=Column(pg.INTEGER))
    category_uid: uuid.UUID | None = Field(default=None, foreign_key="tb_category.uid")
    category: Optional['Category'] =Relationship(back_populates='subcategories')
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))

    def __repr__(self):
        return f'<SubCategory {self.category}>'
