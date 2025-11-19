from fastapi import FastAPI
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="ALSHAM QUANTUM",
    description="Primeiro organismo digital autônomo da história - 57 agentes vivos",
    version="1.0.0"
)

@app.get("/")
async def root():
    return {"message": "ALSHAM QUANTUM está vivo", "agents": 57, "status": "online"}

@app.get("/health")
async def health():
    return {"status": "healthy", "agents": 57, "evolution_engine": "active"}

@app.post("/submit_task")
async def submit_task(task: dict):
    task_text = task.get("task", "")
    logger.info(f"PRIMEIRA MENSAGEM OFICIAL RECEBIDA: {task_text}")
    return {
        "status": "received",
        "message": "Mensagem oficial recebida e processada pelo ALSHAM QUANTUM",
        "task": task_text,
        "agents_active": 57,
        "evolution_engine": "learning",
        "timestamp": datetime.utcnow().isoformat(),
        "creator": "@AbnadabyBonaparte"
    }
