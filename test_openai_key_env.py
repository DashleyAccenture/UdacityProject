#test api key

import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env
load_dotenv('.env')

# Get the key
api_key = os.getenv("OPENAI_API_KEY")
assert api_key, "❌ OPENAI_API_KEY not found in .env file."

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

try:
    # Simple embedding test
    text = "Hello, this is a test for my OpenAI key loaded from .env."
    response = client.embeddings.create(
        model="text-embedding-3-small",  # or "text-embedding-3-large"
        input=text
    )

    # Print results
    vector = response.data[0].embedding
    print("✅ API key works! Embedding length:", len(vector))
    print("First 5 values:", vector[:5])

except Exception as e:
    print("❌ Test failed. Details:")
    print(e)
