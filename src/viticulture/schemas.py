"""
Class responsible for conversion of Viticulture data into dto object
"""
import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class SubCategoryCreateModel(BaseModel):
    """Embrapa SubCategoryCreateModel with subcategories"""
    category_uid: uuid.UUID
    subcategory: str
    control: Optional[str] = None
    product: Optional[str] = None
    country: Optional[str] = None
    qty_product: Optional[float] = None
    vl_product: Optional[float] = None
    year: int


class SubCategoryModel(BaseModel):
    """Embrapa SubCategoryCreateModel with subcategories"""
    category_uid: uuid.UUID
    subcategory: str
    control: Optional[str] = None
    product: Optional[str] = None
    country: Optional[str] = None
    qty_product: Optional[float] = None
    vl_product: Optional[float] = None
    year: int
    created_at: datetime
    updated_at: datetime


class CategoryModel(BaseModel):
    """CategoryModel used for view all user data"""
    uid: uuid.UUID
    category: str
    created_at: datetime
    updated_at: datetime


class CategoryCreateModel(BaseModel):
    """CategoryCreateModel used for registration data"""
    category: str
