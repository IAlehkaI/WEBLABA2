from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.dialects.postgresql import ARRAY
from infrastructure.database import Base
from datetime import datetime

class NewsDB(Base):
    __tablename__ = "news"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    author = Column(String(100), nullable=False)
    content = Column(Text, nullable=False)
    summary = Column(String(500), nullable=False)
    image_url = Column(String(500), nullable=True)
    tags = Column(ARRAY(String), nullable=False, default=[])
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)