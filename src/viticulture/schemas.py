"""
Class responsible for conversion of Viticulture data into dto object
"""
import uuid
from datetime import datetime

from pydantic import BaseModel


class ViticultureModel(BaseModel):
    """ViticultureModel used for view all user data"""
    uid: uuid.UUID
    category: str
    subcategory: str
    data: str
    created_at: datetime
    updated_at: datetime


class ViticultureCreateModel(BaseModel):
    """ViticultureCreateModel used for registration data"""
    category: str
    subcategory: str
    data: str
