from dataclasses import dataclass, field
from datetime import datetime
import uuid


@dataclass
class Post:
    title: str
    content: str
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    author: str = "anonymous"
    created_at: datetime = field(default_factory=datetime.utcnow)
