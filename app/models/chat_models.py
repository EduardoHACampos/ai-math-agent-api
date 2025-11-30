from pydantic import BaseModel

class ChatRequest(BaseModel):
    # Campo obrigatório que recebe a mensagem do usuário
    message: str

class ChatResponse(BaseModel):
    # Campo de resposta devolvido pelo Agente
    response: str