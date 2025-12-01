from fastapi import FastAPI
import uvicorn
from app.routes import chat_routes
from app.config import settings

# Inicialização usando o nome do .env
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.API_VERSION
)

# Registro das rotas
app.include_router(chat_routes.router)

@app.get("/")
def read_root():
    return {
        "status": "online", 
        "project": settings.PROJECT_NAME, 
        "model": settings.MODEL_NAME
    }

if __name__ == "__main__":
    # Inicialização do servidor usando as configs do .env
    uvicorn.run(
        app, 
        host=settings.API_HOST, 
        port=settings.API_PORT
    )