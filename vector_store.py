
from typing import List, Dict, Any
from pathlib import Path
import chromadb
from chromadb import Client
from chromadb.config import Settings
from embeddings import embedding_fn
from models import GameRecord
from settings import DB_PATH

class VectorStoreManager:
    def __init__(self, collection_name: str = "udaplay_games"):
        self.client: Client = chromadb.PersistentClient(path=str(DB_PATH))
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            embedding_function=embedding_fn,
            metadata={"hnsw:space": "cosine"}
        )

    def upsert(self, records: List[GameRecord]) -> int:
        if not records: return 0
        ids = [r.id for r in records]
        documents = [self._document_text(r) for r in records]
        metadatas = [self._metadata(r) for r in records]
        self.collection.upsert(ids=ids, documents=documents, metadatas=metadatas)
        return len(ids)

    def query(self, text: str, top_k: int = 5, where: Dict[str, Any] | None = None) -> Dict[str, Any]:
        include = ["metadatas", "documents", "distances"]
        return self.collection.query(query_texts=[text], n_results=top_k, where=where or {}, include=include)

    @staticmethod
    def _document_text(r: GameRecord) -> str:
        parts = [
            f"Title: {r.title}",
            f"Description: {r.description or ''}",
            f"Genres: {', '.join(r.genres)}",
            f"Developer: {r.developer or ''}",
            f"Publisher: {r.publisher or ''}",
            f"Platforms: {', '.join(r.platforms)}",
            f"Release Date: {r.release_date or ''}",
            f"Source: {r.source}",
            f"URL: {r.url or ''}",
            f"Raw: {r.raw_text or ''}"
        ]
        return "\n".join(parts)

    @staticmethod
    def _metadata(r: GameRecord) -> Dict[str, Any]:
        md = {
            "title": r.title,
            "developer": r.developer or "",
            "publisher": r.publisher or "",
            "platforms": r.platforms,
            "release_date": r.release_date or "",
            "source": r.source,
            "url": r.url or ""
        }
        md.update(r.metadata or {})
        return md
