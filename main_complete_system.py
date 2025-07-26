#!/usr/bin/env python3
"""
Arquivo de redirecionamento para main_complete_system_v2.py
Resolve o problema de nome de arquivo no deploy Railway
"""

# Importa tudo do arquivo v2
from main_complete_system_v2 import *

# Se executado diretamente, roda o main
if __name__ == "__main__":
    import asyncio
    import uvicorn
    
    # Inicia o servidor FastAPI
    uvicorn.run(
        "main_complete_system_v2:app",
        host="0.0.0.0",
        port=8000,
        reload=False
    )
