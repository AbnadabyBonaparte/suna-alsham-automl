from fastapi import FastAPI
from evolution.strategic import daily_evolution
from evolution.quantum import quantum_evolution
from evolution.consciousness import consciousness_evolution

app = FastAPI(title="ALSHAM QUANTUM Backend")

@app.get("/")
async def root():
    return {"message": "ALSHAM QUANTUM Backend - Cérebro Pesado Online"}

@app.post("/evolution/daily")
async def run_daily_evolution():
    return await daily_evolution()

@app.post("/evolution/quantum")
async def run_quantum_evolution():
    return await quantum_evolution()

@app.post("/evolution/consciousness")
async def run_consciousness_evolution():
    return await consciousness_evolution()
