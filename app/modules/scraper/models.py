from pydantic import BaseModel
from typing import List, Dict, Optional, Any
from enum import Enum
from app.core.config.settings import settings


class ScrapeMethod(str, Enum):
    BEAUTIFUL_SOUP = "beautiful_soup"
    REGEX = "regex"


class ScrapedTarget(BaseModel):
    url: str
    method: ScrapeMethod = ScrapeMethod.BEAUTIFUL_SOUP
    selectors: List[str] = []
    headers: Optional[Dict[str, str]] = None
    timeout: int = settings.SCRAPED_TIMEOUT


class ScrapedData(BaseModel):
    url: str
    data: Dict[str, Any]
    timestamp: str
    method_used: ScrapeMethod


class ScrapeResult(BaseModel):
    success: bool
    data: Optional[ScrapedData] = None
    error: Optional[str] = None
    error_code: Optional[str] = None
