
import json, hashlib
from pathlib import Path
from typing import List
from models import GameRecord

def _stable_id(title: str, platforms: List[str]) -> str:
    base = (title.lower().strip() + "|" + "|".join(sorted(p.lower() for p in platforms)))
    return hashlib.sha256(base.encode("utf-8")).hexdigest()[:16]

def load_local_games(data_dir: Path) -> Listrecords: List[GameRecord] = []
    for p in sorted(data_dir.glob("*.json")):
        with p.open("r", encoding="utf-8") as f:
            j = json.load(f)

        # Accept both single record or list in each JSON
        items = j if isinstance(j, list) else [j]
        for it in items:
            title = it.get("title") or it.get("name") or ""
            platforms = it.get("platforms") or it.get("platform") or []
            platforms = platforms if isinstance(platforms, list) else [platforms]
            rec = GameRecord(
                id=_stable_id(title, platforms),
                title=title,
                description=it.get("description", ""),
                genres=it.get("genres", []) or [],
                developer=it.get("developer"),
                publisher=it.get("publisher"),
                platforms=platforms,
                release_date=it.get("release_date") or it.get("released") or it.get("release"),
                source="local",
                url=None,
                raw_text=None,
                metadata={k: str(v) for k, v in it.items() if k not in {"description", "genres", "platforms"}}
            )
            records.append(rec)
    return records
