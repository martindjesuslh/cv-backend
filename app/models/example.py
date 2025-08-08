from pydantic import BaseModel
from typing import Dict, Any


class BaseObject(BaseModel):
    name: str
    data: Dict[str, Any]


class ResponseModel(BaseObject):
    id: str
    createdAt: str
