# API de Chat com Agente de IA e Ferramentas Matemáticas 🤖🧮

Este projeto é uma API desenvolvida com **FastAPI** que integra um Agente de Inteligência Artificial capaz de conduzir conversas naturais e executar cálculos matemáticos com alta precisão.
O sistema utiliza o **Ollama** para rodar modelos LLM localmente (recomendado: Llama 3.1) e implementa o padrão de *Function Calling* para delegar operações matemáticas a uma ferramenta Python segura.

---

## 🚀 Funcionalidades

* **Chat Inteligente:** Conversação natural com compreensão de contexto.
* **Ferramenta Matemática (Math Tool):** Detecta automaticamente quando o usuário faz perguntas que exigem cálculos (somas, multiplicações, trigonometria, etc.) e executa essas operações com precisão via Python.
* **Sistema de Proteção:** Verificações de segurança para evitar alucinações da IA (ex.: tentar calcular palavras) e execução do código matemático em ambiente restrito.
* **Tratamento de Erros:** Respostas claras e padronizadas para falhas de conexão com a LLM ou erros internos.

---

## 🛠️ Tecnologias Utilizadas

* **Python 3.10+**
* **FastAPI**
* **Ollama**
* **Pydantic**

---

## 📋 Pré-requisitos

Antes de começar, certifique-se de ter instalado:

1. **Python 3.10+**
2. **Ollama** rodando na sua máquina

---

## ⚙️ Instalação e Configuração

### 1. Clonar o repositório

```bash
git clone <URL_DO_SEU_REPOSITORIO>
cd ai-math-agent-api
```

### 2. Criar o Ambiente Virtual

**Windows (PowerShell):**

```bash
python -m venv .venv
.venv\Scripts\activate
```

**Linux/Mac (Bash):**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar Dependências

```bash
pip install -r requirements.txt
```

> O `requirements.txt` deve incluir: `fastapi`, `uvicorn`, `ollama`, `python-dotenv`

### 4. Configurar o Modelo no Ollama

Recomendação: **Llama 3.1** (suporte nativo a Tools).

```bash
ollama pull llama3.1
```

### 5. Criar o arquivo `.env`

Crie um arquivo `.env` na raiz do projeto:

```ini
# Modelo a ser usado
MODEL_NAME=llama3.1

# URL do servidor Ollama
OLLAMA_BASE_URL=http://localhost:11434
```

---

## ▶️ Como Executar

### 1. Iniciar o Ollama

```bash
ollama run llama3.1
```

### 2. Iniciar o servidor da API

```bash
python -m uvicorn app.main:app --reload
```

A API ficará disponível em: **[http://127.0.0.1:8000](http://127.0.0.1:8000)**

---

## 🧪 Como Testar

Use a documentação interativa (Swagger UI):

👉 **[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)**

Abra o endpoint **POST /chat**, clique em *Try it out* e envie um JSON.

---

## 📤 Exemplos de Requisição

### Cálculo Matemático (Usa a Math Tool)

```json
{
  "message": "Quanto é 1234 * 5678?"
}
```

### Conversa Geral

```json
{
  "message": "Olá, como você pode me ajudar?"
}
```

### Cálculo Complexo

```json
{
  "message": "Qual é a raiz quadrada de 144?"
}
```

---

## 📂 Estrutura do Projeto

```
app/
│── main.py                # Entrada da aplicação FastAPI
│── config.py              # Configurações e variáveis de ambiente
│
├── routes/                # Endpoints da API
├── services/
│     ├── agent_service.py # Lógica do agente + integração com Ollama
│     └── math_tools.py    # Mecanismo matemático seguro
│
└── models/                # Modelos Pydantic (Request/Response)
```
