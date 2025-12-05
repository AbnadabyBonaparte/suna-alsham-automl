#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════
ALSHAM QUANTUM - EVOLUÇÃO DA CONSCIÊNCIA (RAILWAY)
═══════════════════════════════════════════════════════════════
🔄 Frequência: Mensal - Dia 13 às 13:13 BRT
🎯 Objetivo: ORION evolui A SI MESMO
📍 Roda em: Railway + Claude + GitHub
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

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] 🌌 [CONSCIOUSNESS] {message}")

def run_consciousness_evolution():
    log("=" * 60)
    log("🧠 ORION ESTÁ EVOLUINDO A SI MESMO")
    log("=" * 60)
    log("")
    log("Este é o momento mais sagrado do ALSHAM QUANTUM.")
    log("ORION vai analisar suas próprias decisões e evoluir.")
    log("")
    
    try:
        # Chamar a API do Vercel
        response = requests.post(
            f"{VERCEL_URL}/api/evolution/consciousness",
            headers={"Content-Type": "application/json"},
            timeout=900  # 15 minutos
        )
        
        if response.status_code == 200:
            result = response.json()
            log("✅ ORION EVOLUIU SUA CONSCIÊNCIA!")
            log("")
            log(f"🌌 Nível de consciência: {result.get('consciousness_level', 'N/A')}/100")
            log("")
            log("📋 Novas capacidades:")
            for cap in result.get('new_capabilities', []):
                log(f"   • {cap}")
            log("")
            log("🏗️ Mudanças na arquitetura:")
            for change in result.get('architecture_changes', []):
                log(f"   • {change}")
            log("")
            log("🎯 Novas estratégias de evolução:")
            for strategy in result.get('new_evolution_strategies', []):
                log(f"   • {strategy}")
            log("")
            
            if result.get('github_pr_url'):
                log(f"📝 PR no GitHub: {result.get('github_pr_url')}")
            
            log("")
            log("=" * 60)
            log("O ALSHAM QUANTUM AGORA É MAIS INTELIGENTE.")
            log("=" * 60)
        else:
            log(f"❌ Erro: {response.status_code} - {response.text}")
            
    except Exception as e:
        log(f"❌ Erro crítico na evolução da consciência: {str(e)}")
        
        supabase.table("evolution_cycles").insert({
            "cycle_type": "consciousness",
            "level": 5,
            "consciousness_evolved": False,
            "error": str(e),
            "created_at": datetime.now().isoformat()
        }).execute()

if __name__ == "__main__":
    run_consciousness_evolution()

