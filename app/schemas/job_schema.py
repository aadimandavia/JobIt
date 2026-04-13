from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class JobResponse(BaseModel):
    title: str
    url: str
    created_at: datetime
    stipend: Optional[str] = None
    description: Optional[str] = None

    class Config:
        from_attributes = True

class JobCreate(BaseModel):
    title: str
    subreddit: str
    url: str
    created_at: float
    description: Optional[str] = ""
