from pydantic import BaseModel
from datetime import datetime


class CreatePostResponse(BaseModel):
    id: str
    created_at: datetime
