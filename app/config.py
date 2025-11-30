import os
from dotenv import load_dotenv

# Carrega as variáveis definidas no arquivo .env para o contexto da aplicação
load_dotenv()

class Config:
    # Definição do modelo de LLM (padrão: llama3)
    MODEL_NAME = os.getenv("MODEL_NAME", "llama3")
    
    # URL base para conexão com a API do Ollama
    OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

# Instância exportada para uso nos serviços
settings = Config()