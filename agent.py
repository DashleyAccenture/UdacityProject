
from enum import Enum, auto
from typing import Dict, List
from models import RetrievalHit, GameRecord
from tools import retrieve_game, evaluate_retrieval, game_web_search
from report import build_report
from memory import persist_new_knowledge
from settings import MIN_CONFIDENCE

class AgentState(Enum):
    ASK = auto()
    RAG = auto()
    EVAL = auto()
    WEB = auto()
    PARSE = auto()
    STORE = auto()
    REPORT = auto()

class UdaPlayAgent:
    def __init__(self): pass

    def run(self, question: str) -> Dict[str, str]:
        state = AgentState.ASK
        rag_hits: List[RetrievalHit] = []
        web_records: List[GameRecord] = []
        confidence = 0.0
        metrics = {}
        resolved: Dict[str, str] = {}
        reasoning_steps: List[str] = []

        # RAG
        state = AgentState.RAG
        rag_hits = retrieve_game(question)
        reasoning_steps.append(f"RAG returned {len(rag_hits)} hits.")

        # Evaluate
        state = AgentState.EVAL
        confidence, metrics = evaluate_retrieval(question, rag_hits)
        reasoning_steps.append(f"Evaluation metrics: {metrics} → confidence={confidence:.3f}.")

        # Decide fallback
        if confidence < MIN_CONFIDENCE:
            state = AgentState.WEB
            web_records = game_web_search(question)
            reasoning_steps.append(f"Fallback to web produced {len(web_records)} candidates.")
            state = AgentState.PARSE
            # prefer first web record; refine resolved fields
            best_web = web_records[0] if web_records else None
            if best_web:
                resolved = {
                    "title": best_web.title or _infer_title(question),
                    "developer": best_web.developer or "",
                    "publisher": best_web.publisher or "",
                    "release_date": best_web.release_date or "",
                    "platforms": ", ".join(best_web.platforms) if best_web.platforms else ""
                }
                # store memory
                state = AgentState.STORE
                added = persist_new_knowledge(web_records[:3])
                reasoning_steps.append(f"Persisted {added} new web‑sourced records.")
                # recompute confidence (boost slightly due to fresh authoritative source)
                confidence = min(1.0, max(confidence, 0.72))
        else:
            # Resolve from local hits (majority vote on top 3)
            resolved = _resolve_from_local(question, rag_hits[:3])
            reasoning_steps.append("Resolved facts from local dataset.")

        state = AgentState.REPORT
        from report import render
        report = build_report(
            question=question,
            resolved=resolved,
            confidence=confidence,
            sources_local=rag_hits,
            sources_web=web_records,
            reasoning=" → ".join(reasoning_steps)
        )
        return {"markdown": render(report)}

def _infer_title(question: str) -> str:
    import re
    m = re.search(r"“([^”]+)”|\"([^\"]+)\"", question)
    return m.group(1) or m.group(2) if m else ""

def _resolve_from_local(question: str, hits: List[RetrievalHit]) -> Dict[str, str]:
    # choose best hit and pull structured fields (simple heuristic: highest score)
    if not hits: return {}
    best = sorted(hits, key=lambda h: h.score, reverse=True)[0]
    resolved = {
        "title": best.title,
        "developer": best.record.developer or "",
        "publisher": best.record.publisher or "",
        "release_date": best.record.release_date or "",
        "platforms": ", ".join(best.record.platforms) if best.record.platforms else ""
    }
    return resolved
