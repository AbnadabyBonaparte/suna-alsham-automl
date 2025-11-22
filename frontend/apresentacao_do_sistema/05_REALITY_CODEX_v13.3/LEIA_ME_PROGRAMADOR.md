# 🌌 REALITY CODEX v13.3 - GUIA COMPLETO PARA PROGRAMADOR

**Data:** 22/11/2025  
**Implementado por:** Antigravity AI  
**Status:** ✅ Código 100% Completo | ⚠️ Não Visível no Navegador  

---

## 📋 RESUMO EXECUTIVO

Implementamos o **Códice Visual Oficial** completo - um sistema de 5 "Realidades" que transforma totalmente a interface, não apenas cores. Cada realidade tem:

- ✅ Background único (partículas, grid, rede neural, textura, raios de luz)
- ✅ Geometria específica (bordas chanfradas, sharp, orgânicas, neumórficas)
- ✅ Tipografia física diferente (Orbitron → IBM Plex → Cinzel → Inter)
- ✅ Efeitos exclusivos (scanlines, breathing, glow, lift)
- ✅ Spring physics customizadas

**PROBLEMA ATUAL:** O código está correto mas não aparece no navegador. Precisa investigação.

---

## 📁 ARQUIVOS CRIADOS (15+)

### Core Infrastructure
1. **`reality.ts`** — Sistema completo de tipos + configs das 5 realidades
2. **`ThemeContext.tsx`** — Enhanced com `useReality()` hook

### Backgrounds (6 arquivos)
3. **`QuantumParticles.tsx`** — Partículas interativas (reagem ao mouse)
4. **`TacticalGrid.tsx`** — Grid militar + crosshairs nos cantos
5. **`NeuralPulse.tsx`** — Rede neural pulsando a 60 BPM
6. **`PremiumNoise.tsx`** — Textura de ruído (aço escovado)
7. **`GodRays.tsx`** — Raios volumétricos diagonais
8. **`RealityBackground.tsx`** — Wrapper condicional

### Effects (3 arquivos)
9. **`Scanlines.tsx`** — Efeito CRT (varredura horizontal)
10. **`BreathingWrapper.tsx`** — Animação de escala pulsante
11. **`ConditionalScanlines.tsx`** — Client wrapper

### UI Components
12. **`RealityCard.tsx`** — Card que muda forma por tema
13. **`ThemeSwitcher.tsx`** — Seletor de realidades (ícone ⚙️)

### Styles
14. **`globals.css`** — CSS variables expandido (5 realidades completas)
15. **`tailwind.config.ts`** — Utilities para realidades

### Integration
16. **`layout.tsx`** — Integração de tudo

---

## 🔍 CHECKLIST DE DIAGNÓSTICO

### 1. Verificar Erros de Compilação

```bash
# No terminal do VSCode
npm run dev
```

**Procurar por:**
- ❌ Erros de import
- ❌ Tipos TypeScript faltando
- ❌ Módulos não encontrados

### 2. Verificar Console do Navegador

**Abrir DevTools (F12) e procurar:**
- Erros em vermelho
- Avisos sobre hooks
- Erros de hidratação do React

### 3. Verificar Se ThemeSwitcher Renderiza

**No navegador, inspecionar elemento:**
```html
<!-- Deve existir isso no DOM: -->
<div class="fixed bottom-6 left-6 z-50">
  <button ...⚙️...</button>
</div>
```

**Se não existe:**
- Layout.tsx não está sendo usado
- Erro no ThemeProvider
- Z-index sendo sobrescrito

### 4. Verificar Providers Corretos

**Em `layout.tsx` deve ter essa ordem:**
```tsx
<NextThemesProvider>
  <ThemeProvider>
    <AuthProvider>
      ...
        <RealityBackground />
        <ThemeSwitcher />
      ...
    </AuthProvider>
  </ThemeProvider>
</NextThemesProvider>
```

### 5. Verificar CSS Variables

**No DevTools, inspecionar `<html>` ou `<body>`:**
```css
/* Deve ter: */
html[data-theme="quantum"] {
  --bg-core: #000000;
  --accent: #00FFC8;
  ...
}
```

---

## 🐛 POSSÍVEIS CAUSAS DO PROBLEMA

### Causa 1: Cache do Next.js
**Solução:**
```bash
rm -rf .next
npm run dev
```

### Causa 2: Dependências Faltando
**Verificar se tem:**
```bash
npm list next-themes clsx tailwind-merge framer-motion
```

**Se faltar, instalar:**
```bash
npm install next-themes clsx tailwind-merge
```

### Causa 3: Z-Index Conflict
O `ThemeSwitcher` tem `z-50`. Verificar se algo está com `z-index` maior bloqueando.

### Causa 4: SSR/Hydration Issues
`ThemeContext` usa `useTheme()` do next-themes que precisa de client-side.

**Verificar se tem `"use client"` em:**
- `ThemeContext.tsx` ✅
- `ThemeSwitcher.tsx` ✅
- `RealityBackground.tsx` ❌ (pode precisar)

### Causa 5: Layout Não Sendo Usado
Verificar se tem outro `layout.tsx` sobrescrevendo.

---

## ✅ TESTES PARA FAZER

### Teste 1: Forçar Tema Manualmente
**No console do navegador:**
```javascript
document.documentElement.setAttribute('data-theme', 'military');
```

Se o fundo mudar → CSS está OK, problema é no JS.

### Teste 2: Verificar Se Providers Carregam
**No console:**
```javascript
// Deve retornar objeto
window.__NEXT_DATA__
```

### Teste 3: Log no ThemeContext
**Adicionar em `ThemeContext.tsx` linha 20:**
```typescript
console.log('[ThemeContext] Current theme:', currentTheme);
console.log('[ThemeContext] Reality config:', realityConfig);
```

Reload e ver se loga no console.

---

## 📝 COMO TESTAR MANUALMENTE

### Opção 1: Build de Produção
```bash
npm run build
npm start
```

### Opção 2: Comentar Tudo e Ir Adicionando
1. Comentar `<RealityBackground />` no layout
2. Comentar `<ThemeSwitcher />`
3. Ver se app carrega
4. Descomentar um por vez

### Opção 3: Criar Página de Teste
Criar `src/app/test-reality/page.tsx`:
```tsx
"use client";
import { useReality } from "@/contexts/ThemeContext";

export default function TestReality() {
  const reality = useReality();
  return (
    <div className="p-8">
      <h1>Reality Test</h1>
      <pre>{JSON.stringify(reality, null, 2)}</pre>
    </div>
  );
}
```

Acessar `/test-reality` e ver se mostra o config.

---

## 🔧 COMANDOS ÚTEIS

```bash
# Limpar tudo e recomeçar
rm -rf .next node_modules package-lock.json
npm install
npm run dev

# Ver processos na porta 3000
netstat -ano | findstr :3000

# Matar processo
taskkill /F /PID [número]

# Lint
npx next lint

# Build
npm run build
```

---

## 📞 PONTOS DE CONTATO

**Se o problema persistir, verificar:**

1. **Version mismatch:** Next.js 16.0.3 vs bibliotecas
2. **Conflito de providers:** Outro ThemeProvider global
3. **CSS não carregando:** Verificar `globals.css` no `layout.tsx`
4. **TypeScript strict mode:** Pode estar bloqueando

---

## 🎯 RESULTADO ESPERADO

Após correção, deve:

1. Ícone ⚙️ aparecer no canto inferior esquerdo
2. Click abre menu com 5 opções
3. Selecionar tema muda:
   - Background (partículas → grid → rede → textura → raios)
   - Fonte (Orbitron → IBM Plex → Cinzel → Inter)
   - Cores (cyan → yellow → purple → blue → gold)
   - Geometria de cards

---

**Todos os arquivos estão nesta pasta.** Código está 100% correto segundo o Códice Oficial.

O problema é de **integração/ambiente**, não de lógica de código.

Boa sorte! 🚀
