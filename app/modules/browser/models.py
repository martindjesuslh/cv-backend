from pydantic import BaseModel
from typing import List, Optional, Dict
from enum import Enum


class ActionType(str, Enum):
    CLICK = "click"
    WAIT = "wait"


class BrowserAction(BaseModel):
    type: ActionType
    selector: Optional[str] = None
    wait_time: Optional[float] = None
    timeout: int = 10


class BrowserTask(BaseModel):
    url: str
    actions: List[BrowserAction]
    headless: bool = True
    cookies: Optional[Dict[str, str]] = None
