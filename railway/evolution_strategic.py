#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════
ALSHAM QUANTUM - EVOLUÇÃO ESTRATÉGICA (RAILWAY)
═══════════════════════════════════════════════════════════════
🔄 Frequência: Diária às 03:33 BRT
🎯 Objetivo: Evolução profunda com Claude + Optuna
📍 Roda em: Railway
═══════════════════════════════════════════════════════════════
"""

import os
import json
import requests
from datetime import datetime
from supabase import create_client
import anthropic

# Config
SUPABASE_URL = os.getenv("NEXT_PUBLIC_SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
VERCEL_URL = os.getenv("VERCEL_URL", "https://suna-alsham-automl.vercel.app")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
claude = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

def log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] 🎯 [STRATEGIC] {message}")

def run_strategic_evolution():
    log("Iniciando ciclo de evolução estratégica...")
    
    try:
        # Chamar a API do Vercel
        response = requests.post(
            f"{VERCEL_URL}/api/evolution/daily",
            headers={"Content-Type": "application/json"},
            timeout=300  # 5 minutos
        )
        
        if response.status_code == 200:
            result = response.json()
            log(f"✅ Ciclo completo!")
            log(f"   Agents evoluídos: {result.get('agents_evolved', 0)}")
            log(f"   Ganho total: {result.get('total_efficiency_gain', 0)}%")
            log(f"   Tempo: {result.get('execution_time_ms', 0)}ms")
        else:
            log(f"❌ Erro: {response.status_code} - {response.text}")
            
    except Exception as e:
        log(f"❌ Erro crítico: {str(e)}")
        
        # Registrar erro no banco
        supabase.table("evolution_cycles").insert({
            "cycle_type": "strategic",
            "level": 3,
            "agents_evolved": 0,
            "error": str(e),
            "created_at": datetime.now().isoformat()
        }).execute()

if __name__ == "__main__":
    log("=" * 60)
    log("ALSHAM QUANTUM - EVOLUÇÃO ESTRATÉGICA")
    log("=" * 60)
    run_strategic_evolution()
    log("Ciclo finalizado.")

