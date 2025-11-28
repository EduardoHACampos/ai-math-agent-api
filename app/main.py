from fastapi import FastAPI

app = FastAPI(title="API Chat Agente IA")

@app.get("/")
def read_root():
    return {"status": "online", "message": "A API está rodando!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)