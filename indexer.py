
from settings import DATA_DIR
from data_loader import load_local_games
from vector_store import VectorStoreManager

def build_index():
    vsm = VectorStoreManager()
    records = load_local_games(DATA_DIR)
    count = vsm.upsert(records)
    print(f"Indexed {count} local game records into Chroma at {DATA_DIR}")
