import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Neo4j configuration
    NEO4J_URI = os.getenv("NEO4J_URI", "neo4j+ssc://b451e670.databases.neo4j.io")
    NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
    NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "0KyT7Fxg-mo-R0i1y9jSfOX0NN9L-TTH_X7v1S9J1Qo")

    # LLM configuration
    MODEL_NAME = os.getenv("MODEL_NAME", "mistral:latest")  # For Ollama
    
    # API configuration
    API_HOST = os.getenv("API_HOST", "localhost")
    API_PORT = int(os.getenv("API_PORT", "8000"))
    
    # Frontend configuration
    STREAMLIT_PORT = int(os.getenv("STREAMLIT_PORT", "8501"))
