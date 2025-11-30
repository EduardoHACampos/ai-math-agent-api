import ollama
from app.config import settings
from app.services.math_tools import calculate_expression

math_tool_definition = {
    "type": "function",
    "function": {
        "name": "calculate_expression",
        "description": "Realiza cálculos matemáticos exatos.",
        "parameters": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "A expressão matemática. Ex: '12 * 5'"
                }
            },
            "required": ["expression"]
        }
    }
}

available_functions = {
    "calculate_expression": calculate_expression
}

async def process_message(user_message: str) -> str:
    """
    Orquestra a interação com o modelo com verificação contra alucinações.
    """
    try:
        client = ollama.Client(host=settings.OLLAMA_BASE_URL)

        # Prompt ainda mais agressivo para evitar chamadas indevidas
        system_instructions = (
            "Você é o melhor assistente virtual. "
            "REGRA DE OURO: JAMAIS chame a ferramenta 'calculate_expression' se a mensagem do usuário não contiver números explícitos. "
            "Para 'oi', 'teste', 'olá', apenas responda com texto cordial ou qualquer coisa que nao seja matematica ou exija calculadora."
        )

        messages_payload = [
            {'role': 'system', 'content': system_instructions},
            {'role': 'user', 'content': user_message}
        ]

        response = client.chat(
            model=settings.MODEL_NAME,
            messages=messages_payload,
            tools=[math_tool_definition]
        )

        print(f"\n[DEBUG] IA Decidiu: {response['message']}")

        # Lógica de verificação
        if response.get('message', {}).get('tool_calls'):
            for tool in response['message']['tool_calls']:
                function_name = tool['function']['name']
                function_args = tool['function']['arguments']
                
                expression = function_args.get('expression', '')
                
                # Se a expressão estiver vazia ou NÃO tiver nenhum número
                has_numbers = any(char.isdigit() for char in expression)
                
                if not expression or not has_numbers:
                    print(f"[DEBUG] Bloqueando chamada de ferramenta inválida: {expression}")
                    # Retornamos uma resposta padrão em vez de deixar o erro acontecer
                    return "Entendi sua mensagem, mas não há cálculo a ser feito. Como posso ajudar?"

                # Se passou na verificação, executa a conta
                if function_name in available_functions:
                    function_to_call = available_functions[function_name]
                    tool_output = function_to_call(expression)
                    return f"Resultado do cálculo: {tool_output}"

        # Retorna o conteúdo de texto da IA
        content = response['message']['content']
        
        # Fallback: Se a IA tentou chamar ferramenta (e falhou) e retornou content vazio
        if not content:
            return "Olá! Sou seu assistente virtual. Pode me pedir para calcular algo ou apenas conversar."
            
        return content

    except Exception as e:
        return f"Erro no processamento: {str(e)}"