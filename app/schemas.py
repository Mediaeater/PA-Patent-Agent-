# file: app/schemas.py
from pydantic import BaseModel
from typing import List, Optional

class InventionInput(BaseModel):
    title: Optional[str] = None
    readme_content: str
    prior_art: Optional[List[dict]] = None  # e.g., [{"patent":"US123", "excerpt":"..."}]
    inventor: Optional[List[str]] = None
    jurisdiction: Optional[str] = "USPTO"
    date: Optional[str] = None
