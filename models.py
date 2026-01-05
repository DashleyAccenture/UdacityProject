
from typing import List, Optional, Dict
from pydantic import BaseModel, Field

class GameRecord(BaseModel):
    id: str                                 # stable unique id (hash title+platform)
    title: str
    description: Optional[str] = ""
    genres: List[str] = Field(default_factory=list)
    developer: Optional[str] = None
    publisher: Optional[str] = None
    platforms: List[str] = Field(default_factory=list)
    release_date: Optional[str] = None      # ISO or textual date
    source: str = "local"                   # "local" | "web"
    url: Optional[str] = None               # citation when source == "web"
    raw_text: Optional[str] = None          # full text chunk if web ingested
    metadata: Dict[str, str] = Field(default_factory=dict)

class RetrievalHit(BaseModel):
    id: str
    title: str
    score: float               # similarity (1 - distance) or normalized metric
    record: GameRecord
    source: str                # "local" | "web"

class AnswerReport(BaseModel):
    question: str
    answer: str
    facts: Dict[str, str]      # structured fields resolved
    confidence: float
    citations: List[Dict[str, str]]   # [{source, title, url or 'local dataset'}]
    reasoning: str
