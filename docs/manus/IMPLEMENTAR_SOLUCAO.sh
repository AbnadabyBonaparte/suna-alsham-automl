#!/bin/bash

# ═══════════════════════════════════════════════════════════════
# SCRIPT DE IMPLEMENTAÇÃO AUTOMÁTICA
# Solução: Loop Infinito no Onboarding - ALSHAM QUANTUM
# ═══════════════════════════════════════════════════════════════

set -e  # Parar em caso de erro

FRONTEND_DIR="frontend/src"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

echo "🚀 Iniciando implementação da solução..."
echo ""

# ═══════════════════════════════════════════════════════════════
# 1. VERIFICAR ESTRUTURA
# ═══════════════════════════════════════════════════════════════

echo "📁 Verificando estrutura do projeto..."

if [ ! -d "$FRONTEND_DIR" ]; then
    echo "❌ Erro: Diretório $FRONTEND_DIR não encontrado"
    echo "   Execute este script a partir da raiz do repositório"
    exit 1
fi

if [ ! -f "$FRONTEND_DIR/middleware.ts" ]; then
    echo "❌ Erro: $FRONTEND_DIR/middleware.ts não encontrado"
    exit 1
fi

if [ ! -f "$FRONTEND_DIR/lib/supabase/proxy_FIXED.ts" ]; then
    echo "❌ Erro: $FRONTEND_DIR/lib/supabase/proxy_FIXED.ts não encontrado"
    exit 1
fi

echo "✅ Estrutura verificada"
echo ""

# ═══════════════════════════════════════════════════════════════
# 2. FAZER BACKUP
# ═══════════════════════════════════════════════════════════════

echo "💾 Fazendo backup dos arquivos originais..."

BACKUP_DIR="$FRONTEND_DIR/backups/$TIMESTAMP"
mkdir -p "$BACKUP_DIR"

cp "$FRONTEND_DIR/middleware.ts" "$BACKUP_DIR/middleware.ts.backup"
echo "   ✅ Backup de middleware.ts criado"

if [ -f "$FRONTEND_DIR/lib/supabase/proxy.ts" ]; then
    cp "$FRONTEND_DIR/lib/supabase/proxy.ts" "$BACKUP_DIR/proxy.ts.backup"
    echo "   ✅ Backup de proxy.ts criado"
fi

echo "   📂 Backups salvos em: $BACKUP_DIR"
echo ""

# ═══════════════════════════════════════════════════════════════
# 3. DESABILITAR MIDDLEWARE ANTIGO
# ═══════════════════════════════════════════════════════════════

echo "🔒 Desabilitando middleware antigo..."

mv "$FRONTEND_DIR/middleware.ts" "$FRONTEND_DIR/middleware.ts.DISABLED"
echo "   ✅ middleware.ts renomeado para middleware.ts.DISABLED"
echo ""

# ═══════════════════════════════════════════════════════════════
# 4. IMPLEMENTAR NOVO MIDDLEWARE
# ═══════════════════════════════════════════════════════════════

echo "🔧 Implementando novo middleware..."

# Copiar proxy_FIXED.ts para middleware.ts
cp "$FRONTEND_DIR/lib/supabase/proxy_FIXED.ts" "$FRONTEND_DIR/middleware.ts"
echo "   ✅ proxy_FIXED.ts copiado para middleware.ts"

# Adicionar export config ao final se não existir
if ! grep -q "export const config" "$FRONTEND_DIR/middleware.ts"; then
    cat >> "$FRONTEND_DIR/middleware.ts" << 'EOF'

export const config = {
  matcher: [
    '/((?!_next/static|_next/image|favicon.ico|public|.*\\..*|sounds|images).*)',
  ],
};
EOF
    echo "   ✅ Export config adicionado"
fi

echo ""

# ═══════════════════════════════════════════════════════════════
# 5. VERIFICAR INTEGRIDADE
# ═══════════════════════════════════════════════════════════════

echo "🔍 Verificando integridade dos arquivos..."

if [ ! -f "$FRONTEND_DIR/middleware.ts" ]; then
    echo "❌ Erro: middleware.ts não foi criado"
    exit 1
fi

if ! grep -q "export async function updateSession" "$FRONTEND_DIR/middleware.ts"; then
    echo "❌ Erro: middleware.ts não contém updateSession"
    exit 1
fi

if ! grep -q "export const config" "$FRONTEND_DIR/middleware.ts"; then
    echo "❌ Erro: middleware.ts não contém export config"
    exit 1
fi

echo "   ✅ Arquivo middleware.ts verificado"
echo ""

# ═══════════════════════════════════════════════════════════════
# 6. RESUMO
# ═══════════════════════════════════════════════════════════════

echo "═══════════════════════════════════════════════════════════════"
echo "✅ IMPLEMENTAÇÃO CONCLUÍDA COM SUCESSO!"
echo "═══════════════════════════════════════════════════════════════"
echo ""
echo "📋 Resumo das mudanças:"
echo ""
echo "   1. ✅ Middleware antigo desabilitado"
echo "      → $FRONTEND_DIR/middleware.ts.DISABLED"
echo ""
echo "   2. ✅ Novo middleware implementado"
echo "      → $FRONTEND_DIR/middleware.ts"
echo ""
echo "   3. ✅ Backups criados"
echo "      → $BACKUP_DIR/"
echo ""
echo "═══════════════════════════════════════════════════════════════"
echo ""
echo "🚀 Próximos passos:"
echo ""
echo "   1. Fazer commit das mudanças:"
echo "      git add frontend/src/middleware.ts"
echo "      git add frontend/src/middleware.ts.DISABLED"
echo "      git commit -m 'fix: resolver loop infinito no onboarding'"
echo ""
echo "   2. Fazer deploy:"
echo "      git push origin main"
echo ""
echo "   3. Testar em produção:"
echo "      - Fazer login com novo usuário"
echo "      - Verificar redirecionamento para /onboarding"
echo "      - Completar onboarding"
echo "      - Verificar redirecionamento para /dashboard"
echo ""
echo "   4. Monitorar logs:"
echo "      - Verificar Vercel/Railway logs"
echo "      - Verificar Supabase logs"
echo "      - Verificar console do navegador"
echo ""
echo "═══════════════════════════════════════════════════════════════"
echo ""
echo "📚 Documentação:"
echo "   Veja SOLUCAO_LOOP_INFINITO_ONBOARDING.md para detalhes completos"
echo ""
echo "✅ Implementação pronta!"
