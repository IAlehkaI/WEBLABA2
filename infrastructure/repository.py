import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional
from domain.models import News

DATA_DIR = Path("data")
DATA_FILE = DATA_DIR / "news.json"

class InMemoryNewsRepository:
    def __init__(self, max_size: int = 50):
        self._max_size = max_size
        self._counter = 1
        DATA_DIR.mkdir(exist_ok=True)
        self._load_from_file()

    def _load_from_file(self):
        if DATA_FILE.exists():
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                self._news = [
                    News(
                        id=item["id"],
                        title=item["title"],
                        author=item["author"],
                        content=item["content"],
                        summary=item["summary"],
                        image_url=item.get("image_url", ""),
                        tags=item.get("tags", []),
                        created_at=item["created_at"]
                    )
                    for item in data
                ]
                if self._news:
                    self._counter = max(n.id for n in self._news) + 1
            except (json.JSONDecodeError, KeyError, ValueError) as e:
                print(f"⚠️ Ошибка при загрузке данных: {e}. Создаём пустое хранилище.")
                self._news = []
        else:
            self._news = []
        self._prune()

    def _save_to_file(self):
        data = [
            {
                "id": n.id,
                "title": n.title,
                "author": n.author,
                "content": n.content,
                "summary": n.summary,
                "image_url": n.image_url,
                "tags": n.tags,
                "created_at": n.created_at
            }
            for n in self._news
        ]
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def _prune(self):
        if len(self._news) > self._max_size:
            self._news = sorted(
                self._news,
                key=lambda x: x.created_at,
                reverse=True
            )[:self._max_size]

    def create(self, news: News) -> News:
        news.id = self._counter
        self._counter += 1
        news.created_at = datetime.now(timezone.utc).isoformat()
        self._news.append(news)
        self._prune()
        self._save_to_file()
        return news

    def get_all(self) -> List[News]:
        return sorted(self._news, key=lambda x: x.created_at, reverse=True)

    def get_by_id(self, news_id: int) -> Optional[News]:
        for n in self._news:
            if n.id == news_id:
                return n
        return None

    def update(self, news_id: int, updated_news: News) -> Optional[News]:
        for i, n in enumerate(self._news):
            if n.id == news_id:
                updated_news.id = news_id
                updated_news.created_at = n.created_at
                self._news[i] = updated_news
                self._save_to_file()
                return updated_news
        return None

    def delete(self, news_id: int) -> bool:
        for i, n in enumerate(self._news):
            if n.id == news_id:
                del self._news[i]
                self._save_to_file()
                return True
        return False

    def search(self, query: str) -> List[News]:
        if not query:
            return self.get_all()

        query = query.lower().strip()
        print(f"ПОИСК ПО ЗАПРОСУ: '{query}'")  # ← эта строка покажет, что пришло

        result = []
        for n in self._news:
            if (query in n.title.lower() or
                    query in n.author.lower() or
                    query in n.summary.lower() or
                    query in n.content.lower()):
                print(f"НАЙДЕНО: {n.title}")
                result.append(n)

        return sorted(result, key=lambda x: x.created_at, reverse=True)