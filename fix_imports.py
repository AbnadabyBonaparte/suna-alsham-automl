#!/usr/bin/env python3
"""
Corrige imports quebrados nos agentes CORE
"""
import os
import re

class ImportFixer:
    def __init__(self):
        self.common_fixes = {
            'from jwt import': 'import jwt',
            'import jwt as': 'import jwt',
            'from networkx import': 'import networkx',
            'from jose import': 'from jose import jwt as jose_jwt',
        }
    
    def fix_file_imports(self, file_path):
        """Corrige imports em um arquivo específico"""
        if not os.path.exists(file_path):
            return False
            
        print(f"🔧 Corrigindo imports em: {file_path}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Aplicar correções comuns
        for old_import, new_import in self.common_fixes.items():
            if old_import in content:
                content = content.replace(old_import, new_import)
                print(f"   ✅ Corrigido: {old_import} → {new_import}")
        
        # Salvar se houver mudanças
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"   💾 Arquivo atualizado: {file_path}")
            return True
        
        return False
    
    def fix_all_agents(self):
        """Corrige imports em todos os arquivos de agentes"""
        agent_files = [
            'performance_monitor_agent.py',
            'security_guardian_agent.py', 
            'meta_cognitive_agents.py',
            'system_agents.py',
            'service_agents.py',
            'specialized_agents.py',
            'core_agents_v3.py'
        ]
        
        fixed_count = 0
        for file_path in agent_files:
            if self.fix_file_imports(file_path):
                fixed_count += 1
        
        print(f"\n✅ {fixed_count} arquivos corrigidos!")

if __name__ == "__main__":
    fixer = ImportFixer()
    fixer.fix_all_agents()
