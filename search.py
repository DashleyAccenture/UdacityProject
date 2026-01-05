
from typing import List
from vector_store import VectorStoreManager
from models import RetrievalHit, GameRecord
from settings import TOP_K, HYBRID_METADATA_FILTERS

def semantic_search(query: str) -> Listvsm = VectorStoreManager()
    where = {}  # add filters if HYBRID_METADATA_FILTERS True and you detect intent
    res = vsm.query(query, top_k=TOP_K, where=where)
    hits: List[RetrievalHit] = []
    for idx, doc in enumerate(res["documents"][0]):
        md = res["metadatas"][0][idx]
        distance = res["distances"][0][idx]
        score = max(0.0, 1.0 - distance)     # normalize as similarity
        record = GameRecord(
            id=md.get("id") or md.get("doc_id") or "",  # not always present, keep blank if missing
            title=md.get("title", ""),
            description="", genres=[],
            developer=md.get("developer") or None,
            publisher=md.get("publisher") or None,
            platforms=md.get("platforms", []) or [],
            release_date=md.get("release_date") or None,
            source=md.get("source", "local"),
            url=md.get("url") or None,
        )
        hits.append(RetrievalHit(id=record.id, title=record.title, score=score, record=record, source=record.source))
    return hits
