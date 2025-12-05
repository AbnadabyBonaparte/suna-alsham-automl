#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════
ALSHAM QUANTUM - EVOLUÇÃO QUÂNTICA (RAILWAY)
═══════════════════════════════════════════════════════════════
🔄 Frequência: Semanal - Domingo às 04:44 BRT
🎯 Objetivo: Criar novos agents + Auto-commit no GitHub
📍 Roda em: Railway + GitHub API
═══════════════════════════════════════════════════════════════
"""

import os
import json
import requests
from datetime import datetime
from supabase import create_client

# Config
SUPABASE_URL = os.getenv("NEXT_PUBLIC_SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
VERCEL_URL = os.getenv("VERCEL_URL", "https://suna-alsham-automl.vercel.app")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] ⚛️ [QUANTUM] {message}")

def run_quantum_evolution():
    log("Iniciando ciclo de evolução quântica...")
    log("Este ciclo pode criar novos agents e commitar no GitHub...")
    
    try:
        # Chamar a API do Vercel
        response = requests.post(
            f"{VERCEL_URL}/api/evolution/quantum",
            headers={"Content-Type": "application/json"},
            timeout=600  # 10 minutos
        )
        
        if response.status_code == 200:
            result = response.json()
            log(f"✅ Ciclo quântico completo!")
            log(f"   Agents evoluídos: {result.get('agents_evolved', 0)}")
            log(f"   Agents criados: {result.get('agents_created', 0)}")
            log(f"   PRs no GitHub: {result.get('github_prs_created', 0)}")
            log(f"   Ganho total: {result.get('total_efficiency_gain', 0)}%")
            
            # Listar PRs criados
            for evolution in result.get('evolutions', []):
                if evolution.get('github_pr'):
                    log(f"   📝 PR: {evolution.get('github_pr')}")
        else:
            log(f"❌ Erro: {response.status_code} - {response.text}")
            
    except Exception as e:
        log(f"❌ Erro crítico: {str(e)}")
        
        supabase.table("evolution_cycles").insert({
            "cycle_type": "quantum",
            "level": 4,
            "agents_evolved": 0,
            "error": str(e),
            "created_at": datetime.now().isoformat()
        }).execute()

if __name__ == "__main__":
    log("=" * 60)
    log("ALSHAM QUANTUM - EVOLUÇÃO QUÂNTICA")
    log("⚛️ O SISTEMA VAI EVOLUIR SOZINHO E COMMITAR NO GITHUB")
    log("=" * 60)
    run_quantum_evolution()
    log("Ciclo quântico finalizado.")

