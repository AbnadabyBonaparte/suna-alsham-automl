#!/usr/bin/env python3
"""
Análise Enterprise - Como os agentes devem ser criados
"""

import inspect
import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)8s] %(message)s'
)
logger = logging.getLogger('AgentAnalysis')

def analyze_module(module_name):
    """Analisa estrutura completa de um módulo"""
    logger.info(f"\n{'='*60}")
    logger.info(f"ANALISANDO: {module_name}")
    logger.info(f"{'='*60}")
    
    try:
        module = __import__(module_name)
        
        # 1. Listar todas as classes
        classes = []
        functions = []
        
        for name, obj in inspect.getmembers(module):
            if inspect.isclass(obj) and obj.__module__ == module_name:
                classes.append((name, obj))
            elif inspect.isfunction(obj) and obj.__module__ == module_name:
                functions.append((name, obj))
        
        # 2. Mostrar classes encontradas
        if classes:
            logger.info(f"\n📦 CLASSES ENCONTRADAS ({len(classes)}):")
            for class_name, class_obj in classes:
                logger.info(f"\n  🔸 {class_name}")
                
                # Verificar se é um agente
                if 'Agent' in class_name:
                    # Mostrar init signature
                    try:
                        init_method = class_obj.__init__
                        sig = inspect.signature(init_method)
                        logger.info(f"     __init__{sig}")
                        
                        # Verificar herança
                        bases = [base.__name__ for base in class_obj.__bases__]
                        logger.info(f"     Herda de: {bases}")
                        
                    except Exception as e:
                        logger.error(f"     Erro analisando __init__: {e}")
        
        # 3. Mostrar funções encontradas
        if functions:
            logger.info(f"\n📋 FUNÇÕES ENCONTRADAS ({len(functions)}):")
            for func_name, func_obj in functions:
                sig = inspect.signature(func_obj)
                logger.info(f"  🔹 {func_name}{sig}")
                
                # Se for create_*, mostrar detalhes
                if func_name.startswith('create_'):
                    logger.info(f"     ⚡ FUNÇÃO DE CRIAÇÃO ENCONTRADA!")
                    
                    # Verificar docstring
                    if func_obj.__doc__:
                        logger.info(f"     Docstring: {func_obj.__doc__.strip().split(chr(10))[0]}")
        
        # 4. Procurar padrão de criação no final do arquivo
        logger.info(f"\n🔍 PROCURANDO PADRÃO DE CRIAÇÃO NO CÓDIGO...")
        
        # Ler arquivo fonte
        try:
            import importlib.util
            spec = importlib.util.find_spec(module_name)
            if spec and spec.origin:
                with open(spec.origin, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                
                # Procurar por funções create_ ou def create
                for i, line in enumerate(lines):
                    if 'def create' in line or 'create_agents' in line:
                        logger.info(f"     Linha {i+1}: {line.strip()}")
                        # Mostrar próximas 5 linhas
                        for j in range(1, 6):
                            if i+j < len(lines):
                                logger.info(f"     Linha {i+j+1}: {lines[i+j].strip()}")
                        break
        except Exception as e:
            logger.error(f"     Erro lendo arquivo fonte: {e}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Erro analisando {module_name}: {e}")
        return False

def check_create_pattern():
    """Verifica se existe um padrão comum de criação"""
    logger.info(f"\n{'='*60}")
    logger.info("VERIFICANDO PADRÃO DE CRIAÇÃO")
    logger.info(f"{'='*60}")
    
    # Verificar se existe uma função create_agents em algum lugar
    modules_to_check = [
        'specialized_agents',
        'ai_powered_agents', 
        'core_agents_v3',
        'system_agents'
    ]
    
    for module_name in modules_to_check:
        try:
            module = __import__(module_name)
            
            # Verificar final do arquivo - comum ter create_agents no final
            logger.info(f"\n🔎 Verificando {module_name} por create_* ...")
            
            # Listar TUDO no módulo
            all_items = dir(module)
            create_items = [item for item in all_items if 'create' in item.lower()]
            
            if create_items:
                logger.info(f"   ✅ Itens com 'create': {create_items}")
            else:
                logger.info(f"   ❌ Nenhum item com 'create' encontrado")
                
        except Exception as e:
            logger.error(f"   Erro: {e}")

def main():
    """Análise principal"""
    
    # 1. Analisar estrutura de cada módulo principal
    modules = [
        'specialized_agents',
        'ai_powered_agents',
        'core_agents_v3',
        'system_agents'
    ]
    
    for module in modules:
        analyze_module(module)
    
    # 2. Verificar padrão de criação
    check_create_pattern()
    
    # 3. Sugerir solução
    logger.info(f"\n{'='*60}")
    logger.info("💡 SOLUÇÃO RECOMENDADA")
    logger.info(f"{'='*60}")
    logger.info("""
As classes de agentes existem, mas faltam as funções create_agents().
Precisamos:

1. Adicionar função create_agents() em cada módulo
2. Ou criar um factory pattern centralizado
3. Ou verificar se existe outro arquivo com essas funções

Próximo passo: Verificar se as funções create_agents foram
definidas em outro lugar ou precisam ser criadas.
""")

if __name__ == "__main__":
    main()
