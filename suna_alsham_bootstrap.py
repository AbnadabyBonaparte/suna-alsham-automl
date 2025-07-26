#!/usr/bin/env python3
"""
SUNA-ALSHAM Bootstrap Script - CORRIGIDO
Executa o sistema multi-agente v2.0
"""

import os
import sys
import logging
import subprocess

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger("SUNA-BOOTSTRAP")

def main():
    """Bootstrap que executa o sistema correto"""
    logger.info("🚀 SUNA-ALSHAM Bootstrap Iniciando...")
    logger.info("=" * 60)
    
    # Verificar se o arquivo principal existe
    main_file = "main_complete_system_v2.py"
    
    if os.path.exists(main_file):
        logger.info(f"✅ Arquivo principal encontrado: {main_file}")
        logger.info("🔄 Iniciando sistema multi-agente...")
        
        # Executar o sistema principal
        try:
            subprocess.run([sys.executable, "-u", main_file], check=True)
        except subprocess.CalledProcessError as e:
            logger.error(f"❌ Erro ao executar sistema: {e}")
            sys.exit(1)
    else:
        logger.error(f"❌ Arquivo {main_file} não encontrado!")
        logger.info("📁 Arquivos disponíveis:")
        for f in os.listdir('.'):
            if f.endswith('.py'):
                logger.info(f"  - {f}")
        sys.exit(1)

if __name__ == "__main__":
    main()
