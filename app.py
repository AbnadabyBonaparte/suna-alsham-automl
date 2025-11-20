import os
import json
import random
from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuração de Pastas
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, 'frontend-alsham')

# Fallback para encontrar a pasta correta
if not os.path.exists(FRONTEND_DIR):
    for d in ['frontend-official', 'frontend']:
        if os.path.exists(os.path.join(BASE_DIR, d)):
            FRONTEND_DIR = os.path.join(BASE_DIR, d)
            break

# Rota da API (O Frontend chama isso a cada 2s)
@app.get("/api/telemetry")
async def get_telemetry():
    return {
        "type": "telemetry",
        "system": {
            "cpu": random.randint(20, 65),
            "memory": random.randint(40, 85),
        },
        "business": {
            "roi_current": f"{random.uniform(2800, 3100):.1f}%",
            "savings_generated": f"R$ {random.randint(100, 500)}",
            "transactions_sec": random.randint(45, 120)
        },
        "agents": {
            "active": random.randint(48, 57),
            "total": 57
        },
        "logs": {
            "category": random.choice(["CORE", "SECURITY", "SALES", "NETWORK"]),
            "message": random.choice([
                "Otimizando rede neural...",
                "Transação detectada e processada.",
                "Agente de Vendas iniciou nova campanha.",
                "Varredura de segurança completada: 0 ameaças.",
                "Sincronizando dados com Supabase...",
                "Novo nó de aprendizado criado."
            ])
        }
    }

# Rota Principal - Entrega o HTML
@app.get("/")
async def read_root():
    index_path = os.path.join(FRONTEND_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return JSONResponse({"error": "Frontend not found", "path": FRONTEND_DIR}, status_code=404)

# Arquivos estáticos (se houver CSS/JS separados)
if os.path.exists(FRONTEND_DIR):
    app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
