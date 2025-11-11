from pydantic import BaseModel
from typing import Optional

class Item(BaseModel):
    id: Optional[str] = None
    title: str
    description: str

class ItemResponse(BaseModel):
    id: str
    title: str
    description: str

class ItemUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None