import re

sidebar_path = "src/components/layout/Sidebar.tsx"
with open(sidebar_path, "r", encoding="utf-8") as f:
    content = f.read()

# Inserir o link se não existir
if "/dashboard/evolution" not in content:
    new_link = '  { name: "Evolution Lab", icon: Dna, path: "/dashboard/evolution", color: "text-purple-500" },'
    content = content.replace('{ name: "Neural Nexus"', new_link + '\n  { name: "Neural Nexus"')
    
    # Adicionar import do ícone Dna
    if "Dna," not in content:
        content = content.replace("import {", "import { Dna,")

    with open(sidebar_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("✅ Sidebar atualizada com Evolution Lab")
else:
    print("⚠️ Link já existe na Sidebar")
