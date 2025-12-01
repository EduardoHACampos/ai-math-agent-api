import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # IA
    MODEL_NAME = os.getenv("MODEL_NAME", "llama3.1")
    OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    
    # API / Servidor
    PROJECT_NAME = os.getenv("PROJECT_NAME", "API Chat Agente IA")
    API_HOST = os.getenv("API_HOST", "0.0.0.0")
    API_PORT = int(os.getenv("API_PORT", "8000")) # Convertendo para inteiro
    API_VERSION = os.getenv("API_VERSION", "v1")

settings = Config()