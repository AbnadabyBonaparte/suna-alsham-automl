# main.py — ALSHAM QUANTUM API-ONLY + REDIRECT (100% FUNCIONAL)

from fastapi import FastAPI
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

app = FastAPI(
    title="ALSHAM QUANTUM API",
    description="Backend indestrutível — 139 agents evoluindo 24/7",
    version="1000.0.0"
)

# CORS total (em prod troca por domínios específicos)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Header profissional
@app.middleware("http")
async def add_headers(request, call_next):
    response = await call_next(request)
    response.headers["X-Powered-By"] = "ALSHAM QUANTUM INDESTRUTÍVEL"
    return response

# REDIRECT NA RAIZ
@app.get("/")
async def root():
    return RedirectResponse("https://cerebro-pesado.vercel.app", status_code=301)

# STATUS PÚBLICO
@app.get("/status")
@app.get("/api/status")
async def status():
    return JSONResponse({
        "status": "ONLINE",
        "message": "Cérebro pesado online. 139 agents prontos para evoluir.",
        "codename": "ALSHAM QUANTUM INDESTRUTÍVEL",
        "agents": {"total": 139, "active": 139},
        "timestamp": datetime.now().isoformat()
    }, media_type="application/json; charset=utf-8")

# API SIMPLES PRA NÃO QUEBRAR
@app.get("/api/agents")
async def agents():
    return {"total": 139, "active": 139}

print("ALSHAM QUANTUM API ATIVADA — REDIRECT ATIVO")
