from typing import List
from dataclasses import dataclass

@dataclass
class News:
    id: int
    title: str
    author: str
    content: str
    summary: str
    image_url: str
    tags: List[str]
    created_at: str