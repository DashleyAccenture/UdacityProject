
import os, re
from typing import List, Tuple, Dict
from dotenv import load_dotenv
from tavily import TavilyClient
from models import RetrievalHit, GameRecord
from search import semantic_search
from vector_store import VectorStoreManager
from settings import MIN_CONFIDENCE, TAVILY_MAX_RESULTS, TAVILY_INCLUDE_RAW, COVERAGE_WEIGHT, RELEVANCE_WEIGHT, CONSENSUS_WEIGHT

# --- Retrieve (RAG) ---
def retrieve_game(query: str, k: int = 5) -> Listreturn semantic_search(query)

# --- Evaluate ---
def evaluate_retrieval(question: str, hits: List[RetrievalHit]) -> Tuple[float, Dict[str, float]]:
    if not hits: return 0.0, {"coverage":0,"relevance":0,"consensus":0}

    # Infer intent fields from question
    q = question.lower()
    need_dev = "who developed" in q or "developer" in q
    need_release = "when was" in q or "release date" in q or "released" in q
    need_platform = "platform" in q or "launched on" in q

    # Coverage: do top results contain required fields?
    top = hits[:3]
    coverage_checks = []
    for h in top:
        c = 1.0
        if need_dev and not h.record.developer: c -= 0.5
        if need_release and not h.record.release_date: c -= 0.5
        if need_platform and not h.record.platforms: c -= 0.5
        coverage_checks.append(max(0.0, c))
    coverage = sum(coverage_checks)/len(coverage_checks)

    # Relevance: average similarity of top hits
    relevance = sum(h.score for h in top)/max(1, len(top))

    # Consensus: agreement across top hits on key fields
    def majority(values: List[str]) -> float:
        vals = [v.strip().lower() for v in values if v]
        if not vals: return 0.0
        from collections import Counter
        cnt = Counter(vals)
        return cnt.most_common(1)[0][1] / len(vals)

    dev_cons = majority([h.record.developer for h in top]) if need_dev else 1.0
    rel_cons = majority([h.record.release_date for h in top]) if need_release else 1.0
    plat_cons = majority([", ".join(h.record.platforms) for h in top]) if need_platform else 1.0
    consensus = (dev_cons + rel_cons + plat_cons) / (3 if (need_dev or need_release or need_platform) else 1)

    # Weighted confidence
    confidence = (coverage * COVERAGE_WEIGHT) + (relevance * RELEVANCE_WEIGHT) + (consensus * CONSENSUS_WEIGHT)
    return confidence, {"coverage":coverage, "relevance":relevance, "consensus":consensus}

# --- Web search fallback ---
def game_web_search(question: str) -> Listload_dotenv('.env')
    client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

    res = client.search(
        question,
        max_results=TAVILY_MAX_RESULTS,
        include_raw_content=TAVILY_INCLUDE_RAW
    )

    parsed: List[GameRecord] = []
    for item in res.get("results", []):
        url = item.get("url")
        title = item.get("title") or ""
        content = item.get("content") or ""
        # naive extraction patterns
        dev = _extract(content, r"(?:Developer|Developed by)\s*[:\-]\s*([^\n|,]+)")
        pub = _extract(content, r"(?:Publisher|Published by)\s*[:\-]\s*([^\n|,]+)")
        release = _extract(content, r"(?:Release date|Released on)\s*[:\-]\s*([^\n|,]+)")
        platforms = _extract_platforms(content)
        record = GameRecord(
            id="web-"+hash(url),
            title=_choose_title(question, title, content),
            description=None,
            genres=[],
            developer=dev,
            publisher=pub,
            platforms=platforms,
            release_date=release,
            source="web",
            url=url,
            raw_text=content
        )
        parsed.append(record)
    return parsed

def _extract(text: str, pattern: str) -> str | None:
    m = re.search(pattern, text, flags=re.IGNORECASE)
    return m.group(1).strip() if m else None

def _extract_platforms(text: str) -> List# very basic platform detection
    plats = []
    for p in ["PlayStation", "PS4", "PS5", "Xbox", "Xbox One", "Xbox Series X|S", "PC", "Windows", "Nintendo Switch", "Game Boy", "iOS", "Android"]:
        if re.search(rf"\b{re.escape(p)}\b", text, flags=re.IGNORECASE):
            plats.append(p)
    return sorted(set(plats))

def _choose_title(question: str, page_title: str, content: str) -> str:
    # prefer the page title if it starts with game name; fallback to first quoted phrase in question
    m = re.search(r"“([^”]+)”|\"([^\"]+)\"", question)
    return page_title if page_title else (m.group(1) or m.group(2) if m else page_title)
