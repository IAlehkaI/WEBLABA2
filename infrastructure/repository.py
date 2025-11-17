from typing import List, Optional
from sqlalchemy.orm import Session
from infrastructure.models import NewsDB
from domain.models import News

class PostgreSQLNewsRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, news: News) -> News:
        db_news = NewsDB(
            title=news.title,
            author=news.author,
            content=news.content,
            summary=news.summary,
            image_url=news.image_url,
            tags=news.tags,
        )
        self.db.add(db_news)
        self.db.commit()
        self.db.refresh(db_news)
        return News(
            id=db_news.id,
            title=db_news.title,
            author=db_news.author,
            content=db_news.content,
            summary=db_news.summary,
            image_url=db_news.image_url,
            tags=db_news.tags,
            created_at=db_news.created_at.isoformat()
        )

    def get_all(self) -> List[News]:
        db_news = self.db.query(NewsDB).order_by(NewsDB.created_at.desc()).all()
        return [
            News(
                id=n.id,
                title=n.title,
                author=n.author,
                content=n.content,
                summary=n.summary,
                image_url=n.image_url,
                tags=n.tags,
                created_at=n.created_at.isoformat()
            )
            for n in db_news
        ]

    # Аналогично реализуй get_by_id, update, delete, search
    # ...

    def search(self, query: str) -> List[News]:
        if not query.strip():
            return self.get_all()
        query = query.lower()
        results = self.db.query(NewsDB).filter(
            (NewsDB.title.ilike(f"%{query}%")) |
            (NewsDB.author.ilike(f"%{query}%")) |
            (NewsDB.summary.ilike(f"%{query}%")) |
            (NewsDB.content.ilike(f"%{query}%"))
        ).order_by(NewsDB.created_at.desc()).all()
        return [self._to_domain(n) for n in results]

    def _to_domain(self, db_news: NewsDB) -> News:
        return News(
            id=db_news.id,
            title=db_news.title,
            author=db_news.author,
            content=db_news.content,
            summary=db_news.summary,
            image_url=db_news.image_url,
            tags=db_news.tags,
            created_at=db_news.created_at.isoformat()
        )