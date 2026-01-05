# tools_retrieve.py

# --- Udacity workspace sqlite shim (only needed in Udacity) ---
import importlib.util
import sys

if importlib.util.find_spec("pysqlite3") is not None and "sqlite3" not in sys.modules:
    import pysqlite3
    sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")

import chromadb

# Initialize (or reuse via imports if you already did this elsewhere)
# NOTE: Adjust path if your DB is elsewhere, e.g., ".chroma"
chroma_client = chromadb.PersistentClient(path="chromadb")

# Use the collection name required by your project (e.g., "udaplay" or "udacity")
collection = chroma_client.get_or_create_collection(
    name="udaplay",
    # embedding_function=embedding_fn  # uncomment if you configured server-side embeddings
)


def retrieve_game(query: str, n_results: int = 5) -> list[dict]:
    """
    Semantic search: Finds most relevant results in the vector DB.

    Args:
        query: A question or description about games (platforms, names, years, etc.).
        n_results: How many top matches to return.

    Returns:
        A list of dicts, each containing:
            - Platform
            - Name
            - YearOfRelease
            - Description
            - id (the Chroma document id)
            - score (similarity score derived from distance; higher is better)
            - document (optional raw document string)
    """
    if not query or not isinstance(query, str):
        raise ValueError("`query` must be a non-empty string.")

    # Chroma query returns lists grouped by each input item in query_texts.
    res = collection.query(
        query_texts=[query],
        n_results=n_results,
        include=["metadatas", "documents", "distances"],
    )

    # Defensive extraction: nested lists (one list per query)
    metadatas = res.get("metadatas", [[]])[0]
    documents = res.get("documents", [[]])[0]
    ids = res.get("ids", [[]])[0]
    distances = res.get("distances", [[]])[0]

    results: list[dict] = []
    for i in range(len(ids)):
        meta = metadatas[i] if i < len(metadatas) else {}
        doc = documents[i] if i < len(documents) else ""
        dist = distances[i] if i < len(distances) else None

        # Convert Chroma distance → 0..1 similarity (cosine distance: 0 is identical)
        score = None if dist is None else (1.0 - max(0.0, min(float(dist), 1.0)))

        # Normalize metadata keys expected from your add loop
        results.append(
            {
                "Platform": meta.get("Platform"),
                "Name": meta.get("Name"),
                "YearOfRelease": meta.get("YearOfRelease"),
                "Description": meta.get("Description"),
                "id": ids[i],
                "score": score,
                "document": doc,  # optional (handy for keyword heuristics / debugging)
            }
        )

    return results
