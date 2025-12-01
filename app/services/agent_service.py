import ollama
import json
from app.config import settings
from app.services.math_tools import calculate_expression

math_tool_definition = {
    "type": "function",
    "function": {
        "name": "calculate_expression",
        "description": "Ferramenta exclusiva para CÁLCULOS MATEMÁTICOS (soma, subtração, expressões).",
        "parameters": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "A conta a ser calculada. Ex: '10 * 5'"
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
    Orquestra a interação, trata alucinações de ferramentas e limpa respostas JSON indesejadas.
    """
    try:
        client = ollama.Client(host=settings.OLLAMA_BASE_URL)

        system_instructions = (
            "Você é um assistente útil e direto. "
            "SUAS REGRAS:"
            "1. Você tem APENAS UMA ferramenta: 'calculate_expression'. NUNCA invente outras ferramentas (como text_response)."
            "2. Se for cálculo (números), use a ferramenta."
            "3. Se for conversa (história, geografia, curiosidades), RESPONDA APENAS COM TEXTO NORMAL."
            "4. NÃO retorne JSON para perguntas gerais."
        )

        messages_payload = [
            {'role': 'system', 'content': system_instructions},
            {'role': 'user', 'content': user_message}
        ]

        # 1. Primeira chamada
        response = client.chat(
            model=settings.MODEL_NAME,
            messages=messages_payload,
            tools=[math_tool_definition]
        )

        # 2. Verifica se houve chamada de ferramenta (Real ou Alucinada)
        if response.get('message', {}).get('tool_calls'):
            for tool in response['message']['tool_calls']:
                function_name = tool['function']['name']
                function_args = tool['function']['arguments']
                
                # Nós forçamos a IA a responder de novo, mas SEM ferramentas.
                if function_name not in available_functions:
                    print(f"[DEBUG] Ferramenta inventada detectada ({function_name}). Forçando resposta textual...")
                    response_retry = client.chat(
                        model=settings.MODEL_NAME,
                        messages=messages_payload,
                    )
                    return response_retry['message']['content']

                # Lógica para ferramenta real (Calculadora)
                expression = function_args.get('expression', '')
                has_numbers = any(char.isdigit() for char in expression)
                
                # Verificação: Se tentar calcular texto, força retry textual
                if not expression or not has_numbers:
                    print(f"[DEBUG] Tentativa de calcular texto ('{expression}'). Forçando resposta textual...")
                    response_retry = client.chat(
                        model=settings.MODEL_NAME,
                        messages=messages_payload
                    )
                    return response_retry['message']['content']

                # Se chegou aqui, é um cálculo válido
                function_to_call = available_functions[function_name]
                tool_output = function_to_call(expression)
                return f"Resultado do cálculo: {tool_output}"

        # 3. Tratamento de Conteúdo (Se não houve tool_calls)
        content = response['message']['content']
        
        if content and content.strip().startswith('{'):
            try:
                json_content = json.loads(content)
                # Se parecer uma chamada de ferramenta vazada no texto, fazemos o retry
                if "name" in json_content or "parameters" in json_content:
                    print("[DEBUG] JSON alucinado detectado no texto. Forçando nova resposta...")
                    response_retry = client.chat(
                        model=settings.MODEL_NAME,
                        messages=messages_payload
                    )
                    return response_retry['message']['content']
            except:
                pass

        if not content:
            return "Olá! Ocorreu um erro silencioso, mas estou online. Tente perguntar novamente."
            
        return content

    except Exception as e:
        return f"Erro no processamento: {str(e)}"