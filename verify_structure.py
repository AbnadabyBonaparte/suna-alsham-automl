#!/usr/bin/env python3
"""
Script para verificar a estrutura do repositório SUNA-ALSHAM
Mostra onde estão todos os arquivos de agentes
"""

import os
import json

def find_agent_files(start_dir='.'):
    """Encontra todos os arquivos de agentes no projeto"""
    
    # Lista de arquivos de agentes esperados
    expected_agents = [
        'multi_agent_network.py',
        'specialized_agents.py',
        'ai_powered_agents.py',
        'core_agents_v3.py',
        'system_agents.py',
        'service_agents.py',
        'meta_cognitive_agents.py',
        'code_analyzer_agent.py',
        'web_search_agent.py',
        'code_corrector_agent.py',
        'performance_monitor_agent.py',
        'guard_service.py',
        'guard_agent.py',
        'learn_agent.py'
    ]
    
    # Dicionário para armazenar resultados
    results = {
        'found_in_root': [],
        'found_in_subdirs': {},
        'not_found': [],
        'all_python_files': []
    }
    
    # Procurar arquivos
    for root, dirs, files in os.walk(start_dir):
        # Ignorar diretórios especiais
        if any(skip in root for skip in ['.git', '__pycache__', 'venv', '.env', 'node_modules']):
            continue
            
        for file in files:
            if file.endswith('.py'):
                rel_path = os.path.relpath(root, start_dir)
                full_path = os.path.join(rel_path, file) if rel_path != '.' else file
                results['all_python_files'].append(full_path)
                
                # Verificar se é um agente esperado
                if file in expected_agents:
                    if rel_path == '.':
                        results['found_in_root'].append(file)
                    else:
                        results['found_in_subdirs'][file] = rel_path
    
    # Verificar quais não foram encontrados
    for agent in expected_agents:
        found = False
        if agent in results['found_in_root']:
            found = True
        elif agent in results['found_in_subdirs']:
            found = True
        
        if not found:
            results['not_found'].append(agent)
    
    return results

def print_results(results):
    """Imprime os resultados de forma organizada"""
    
    print("🔍 VERIFICAÇÃO DA ESTRUTURA DO SUNA-ALSHAM")
    print("=" * 60)
    
    # Arquivos na raiz
    print(f"\n✅ AGENTES NA RAIZ ({len(results['found_in_root'])}):")
    for agent in sorted(results['found_in_root']):
        print(f"  ✓ {agent}")
    
    # Arquivos em subdiretórios
    if results['found_in_subdirs']:
        print(f"\n📁 AGENTES EM SUBDIRETÓRIOS ({len(results['found_in_subdirs'])}):")
        for agent, location in sorted(results['found_in_subdirs'].items()):
            print(f"  📍 {agent} → {location}/")
    
    # Arquivos não encontrados
    if results['not_found']:
        print(f"\n❌ AGENTES NÃO ENCONTRADOS ({len(results['not_found'])}):")
        for agent in sorted(results['not_found']):
            print(f"  ✗ {agent}")
    
    # Resumo
    print("\n" + "=" * 60)
    print("📊 RESUMO:")
    print(f"  Total de arquivos Python: {len(results['all_python_files'])}")
    print(f"  Agentes na raiz: {len(results['found_in_root'])}")
    print(f"  Agentes em subdirs: {len(results['found_in_subdirs'])}")
    print(f"  Agentes faltando: {len(results['not_found'])}")
    
    # Comandos sugeridos para mover arquivos
    if results['found_in_subdirs']:
        print("\n🔧 COMANDOS PARA MOVER ARQUIVOS PARA A RAIZ:")
        for agent, location in sorted(results['found_in_subdirs'].items()):
            print(f"  mv {location}/{agent} ./")

def save_results(results):
    """Salva os resultados em um arquivo JSON"""
    with open('structure_report.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print("\n💾 Relatório salvo em: structure_report.json")

def main():
    """Função principal"""
    results = find_agent_files()
    print_results(results)
    save_results(results)

if __name__ == "__main__":
    main()
