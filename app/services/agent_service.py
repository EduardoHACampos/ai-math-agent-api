import ollama
from app.config import settings
from app.services.math_tools import calculate_expression

# Definição do esquema da ferramenta para o entendimento do modelo (Function Calling)
# O modelo utiliza este JSON para decidir quando chamar a função
math_tool_definition = {
    "type": "function",
    "function": {
        "name": "calculate_expression",
        "description": "Realiza cálculos matemáticos precisos. Útil para somas, multiplicações, raízes quadradas, etc.",
        "parameters": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "A expressão matemática a ser calculada. Ex: '12 * 5' ou 'sqrt(144)'"
                }
            },
            "required": ["expression"]
        }
    }
}

# Mapa de funções disponíveis para execução pelo agente
available_functions = {
    "calculate_expression": calculate_expression
}

async def process_message(user_message: str) -> str:
    """
    Orquestra a interação entre a mensagem do usuário, o modelo Ollama e as ferramentas.
    """
    try:
        # Inicialização do cliente Ollama apontando para a URL configurada
        client = ollama.Client(host=settings.OLLAMA_BASE_URL)

        # Envio da mensagem inicial para o modelo com a definição das ferramentas disponíveis
        # O parâmetro 'tools' informa ao modelo o que ele pode utilizar
        response = client.chat(
            model=settings.MODEL_NAME,
            messages=[{'role': 'user', 'content': user_message}],
            tools=[math_tool_definition]
        )

        # Verificação de chamadas de ferramenta na resposta do modelo
        if response.get('message', {}).get('tool_calls'):
            
            # Iteração sobre as ferramentas solicitadas pelo modelo
            for tool in response['message']['tool_calls']:
                function_name = tool['function']['name']
                function_args = tool['function']['arguments']

                # Validação e execução da função mapeada
                if function_name in available_functions:
                    function_to_call = available_functions[function_name]
                    
                    # Execução da ferramenta de cálculo
                    tool_output = function_to_call(function_args.get('expression'))
                    
                    # Retorno apenas do resultado do cálculo para simplificação (neste teste)
                    # Em um chat real, esse resultado voltaria ao modelo para gerar uma frase final
                    return f"Resultado do cálculo: {tool_output}"

        # Retorno da resposta textual padrão caso nenhuma ferramenta tenha sido acionada
        return response['message']['content']

    except Exception as e:
        return f"Falha no processamento do agente: {str(e)}"