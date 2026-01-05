
from pathlib import Path

# --- Paths ---
PROJECT_ROOT = Path(__file__).parent
DB_PATH = PROJECT_ROOT / ".chroma"
DATA_DIR = PROJECT_ROOT / "data" / "games"   # adjust if your dataset lives elsewhere

# --- Embeddings ---
EMBED_MODEL = "text-embedding-3-small"       # high‑quality: "text-embedding-3-large"

# --- Search behavior ---
TOP_K = 5
HYBRID_METADATA_FILTERS = True

# --- Evaluation thresholds (tune to taste) ---
MIN_CONFIDENCE = 0.67       # below this → web fallback
COVERAGE_WEIGHT = 0.35
RELEVANCE_WEIGHT = 0.40
CONSENSUS_WEIGHT = 0.25

# --- Tavily ---
TAVILY_MAX_RESULTS = 5
TAVILY_INCLUDE_RAW = True
