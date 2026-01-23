import os
from google import genai
from google.genai import types
from mem0 import Memory
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(env_path)

GEMINI_API_KEY = os.getenv("GOOGLE_GEMINI_API")
assert GEMINI_API_KEY, "GOOGLE_GEMINI_API not loaded"


NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
assert NEO4J_PASSWORD, "NEO4J_PASSWORD Not Loaded"

# Initialize the Native Gemini Client
client = genai.Client(api_key=GEMINI_API_KEY)

# Mem0 Configuration for Gemini
config = {
    "version": "v1.1",
    "llm": {
        "provider": "gemini",
        "config": {
            "model": "gemini-2.5-flash",
            "temperature": 0.2,
            "api_key": os.environ["GOOGLE_GEMINI_API"]
        }
    },
    "embedder": {
        "provider": "gemini",
        "config": {
            "model": "text-embedding-004", 
            "api_key": os.environ["GOOGLE_GEMINI_API"]
            # REMOVED: task_type and output_dimensionality
        }
    },
    "graph_store":{
        "provider": "neo4j",
        "config": {
            "url":"neo4j+s://c25904f1.databases.neo4j.io",
            "username":NEO4J_USERNAME,
            "password":NEO4J_PASSWORD,      
        }          
    },
    "vector_store": {
        "provider": "qdrant",
        "config": {
            "collection_name": "aaron_memory_768", # New name to reset dimensions
            "host": "localhost",
            "port": 6333,
            "embedding_model_dims": 768
        }
    }
}

memory_client = Memory.from_config(config)

# Interaction loop
user_query = input("> ")

# Generate content using the Native Gemini SDK
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=user_query
)

ai_response = response.text
print(f"AI: {ai_response}")

# Save to Mem0
memory_client.add(
    user_id="tps",
    messages=[
        {"role": "user", "content": user_query},
        {"role": "assistant", "content": ai_response}
    ]
)

print("Memory saved")