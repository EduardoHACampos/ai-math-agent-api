from fastapi import FastAPI
from app.routes import chat_routes

# Inicialização da aplicação
app = FastAPI(title="API Chat Agente IA")

# Registro das rotas (Controllers) na aplicação principal
app.include_router(chat_routes.router)

# Endpoint de verificação de saúde (Health Check)
@app.get("/")
def read_root():
    return {"status": "online", "message": "A API está rodando com Agentes!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)