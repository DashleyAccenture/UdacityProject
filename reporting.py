
from typing import List, Dict
from models import AnswerReport, RetrievalHit, GameRecord

def build_report(question: str, resolved: Dict[str, str], confidence: float,
                 sources_local: List[RetrievalHit], sources_web: List[GameRecord],
                 reasoning: str) -> AnswerReport:
    citations = []
    for h in sources_local[:3]:
        citations.append({"source":"local", "title":h.title, "url":"local dataset"})
    for w in sources_web[:3]:
        citations.append({"source":"web", "title":w.title or resolved.get("title",""), "url": w.url or ""})

    # human‑readable answer based on resolved fields
    bits = []
    if resolved.get("title"): bits.append(f"**{resolved['title']}**")
    if resolved.get("developer"): bits.append(f"developed by {resolved['developer']}")
    if resolved.get("release_date"): bits.append(f"released on {resolved['release_date']}")
    if resolved.get("platforms"): bits.append(f"on {resolved['platforms']}")
    answer = ", ".join(bits) if bits else "See details below."

    return AnswerReport(
        question=question,
        answer=answer,
        facts=resolved,
        confidence=round(confidence, 3),
        citations=citations,
        reasoning=reasoning
    )

def render(report: AnswerReport) -> str:
    # Markdown output
    facts_lines = "\n".join([f"- **{k.replace('_',' ').title()}**: {v}" for k,v in report.facts.items() if v])
    cites_lines = "\n".join([f"- {c['source'].title()}: {c['title']} ({c['url']})" for c in report.citations if c.get("title")])
    md = f"""### UdaPlay Answer
**Question:** {report.question}

**Answer:** {report.answer}

**Confidence:** {report.confidence}

#### Facts
{facts_lines}

#### Citations
{cites_lines}

#### Reasoning
{report.reasoning}
"""
    return md
