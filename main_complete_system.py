#!/usr/bin/env python3
"""
Arquivo de redirecionamento para main_complete_system_v2.py
Resolve o problema de nome de arquivo
"""

# Importa tudo do arquivo v2
from main_complete_system_v2 import *

# Se executado diretamente, roda o main
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
