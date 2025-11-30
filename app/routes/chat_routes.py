from fastapi import APIRouter, HTTPException
from app.models.chat_models import ChatRequest, ChatResponse
from app.services.agent_service import process_message

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Endpoint responsável pelo processamento de mensagens.
    Gerencia validação de entrada, orquestração de serviços e padronização de erros.
    """
    # Validação preliminar do payload de entrada
    if not request.message.strip():
        raise HTTPException(
            status_code=400, 
            detail="A mensagem não pode estar vazia."
        )

    try:
        # Delegação do processamento para a camada de serviço (Agente)
        ai_response = await process_message(request.message)
        
        return ChatResponse(response=ai_response)

    except ConnectionError:
        # Registro interno de falha de conexão com serviços externos (ex: Ollama)
        print("Erro crítico: Falha na conexão com o serviço de LLM.")
        
        raise HTTPException(
            status_code=503, 
            detail="O serviço de IA está indisponível no momento."
        )

    except Exception as e:
        # Captura de exceções não tratadas para registro de log interno
        print(f"Erro interno não tratado: {str(e)}")
        
        # Retorno de erro genérico para evitar vazamento de informações sensíveis
        raise HTTPException(
            status_code=500, 
            detail="Ocorreu um erro interno ao processar a solicitação."
        )