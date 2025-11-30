import math

def calculate_expression(expression: str) -> str:
    """
    Realiza a avaliação segura de expressões matemáticas.
    Utiliza uma whitelist de funções permitidas para evitar execução de código arbitrário.
    """
    try:
        # Mapeamento de funções matemáticas permitidas
        # Restringe o escopo de execução do eval() para segurança
        allowed_names = {
            "sqrt": math.sqrt,
            "sin": math.sin,
            "cos": math.cos,
            "tan": math.tan,
            "pi": math.pi,
            "e": math.e,
            "abs": abs,
            "round": round
        }
        
        # Execução da expressão no contexto restrito
        # __builtins__: None remove acesso a funções nativas perigosas (ex: open, exit)
        result = eval(expression, {"__builtins__": None}, allowed_names)
        
        return str(result)
        
    except SyntaxError:
        return "Erro: Sintaxe matemática inválida."
    except ZeroDivisionError:
        return "Erro: Tentativa de divisão por zero."
    except Exception as e:
        return f"Erro no processamento: {str(e)}"