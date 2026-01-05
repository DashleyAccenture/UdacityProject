
import os
from dotenv import load_dotenv
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction

# Load environment keys
load_dotenv('.env')
OPENAI_API_KEY = ('openai_key')

# Known‑good usage for chromadb>=1.0.4 + openai>=1.73.0
embedding_fn = OpenAIEmbeddingFunction(
    api_key = OPENAI_API_KEY,
    model_name="text-embedding-3-small"
)
