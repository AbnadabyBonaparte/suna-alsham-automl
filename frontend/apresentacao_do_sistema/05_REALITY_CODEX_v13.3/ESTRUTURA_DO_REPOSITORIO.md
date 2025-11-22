# 🌳 ESTRUTURA COMPLETA DO REPOSITÓRIO - ALSHAM QUANTUM v13.3

**Repositório:** `suna-alsham-automl/frontend`  
**Última Atualização:** 22/11/2025 - Reality Codex v13.3  
**Status:** ✅ Commitado e enviado ao GitHub

---

## 📁 ESTRUTURA PRINCIPAL

```
suna-alsham-automl/frontend/
│
├── 📦 node_modules/                    # Dependências (não versionado)
├── 📂 public/                          # Assets públicos
│   ├── sounds/
│   │   └── glitch.mp3                  # Som de transição entre realidades
│   └── ...
│
├── 📂 src/                             # Código fonte
│   │
│   ├── 📂 app/                         # Next.js App Router
│   │   ├── layout.tsx                  # ✨ ROOT LAYOUT - Integração Reality Codex
│   │   ├── page.tsx                    # Landing page
│   │   ├── globals.css                 # ✨ CSS EXPANDIDO - 5 Realidades completas
│   │   │
│   │   └── 📂 dashboard/               # Área principal
│   │       ├── layout.tsx              # Layout do dashboard
│   │       ├── page.tsx                # Cockpit principal
│   │       │
│   │       ├── 📂 agents/              # Sentinelas
│   │       │   └── page.tsx
│   │       │
│   │       ├── 📂 nexus/               # Nexus 3D
│   │       │   └── page.tsx
│   │       │
│   │       ├── 📂 matrix/              # Matrix Terminal
│   │       │   └── page.tsx
│   │       │
│   │       ├── 📂 evolution/           # Evolution Lab
│   │       │   └── page.tsx
│   │       │
│   │       ├── 📂 value/               # Value Dashboard
│   │       │   └── page.tsx
│   │       │
│   │       ├── 📂 void/                # The Void (Easter Egg)
│   │       │   └── page.tsx
│   │       │
│   │       └── 📂 gamification/        # Sistema de Gamificação
│   │           └── page.tsx
│   │
│   ├── 📂 components/                  # Componentes React
│   │   │
│   │   ├── 📂 backgrounds/             # ✨ NOVO - Reality Codex Backgrounds
│   │   │   ├── QuantumParticles.tsx    # Partículas interativas (Quantum)
│   │   │   ├── TacticalGrid.tsx        # Grid militar + crosshairs (Military)
│   │   │   ├── NeuralPulse.tsx         # Rede neural 60bpm (Neural)
│   │   │   ├── PremiumNoise.tsx        # Textura premium (Titanium)
│   │   │   ├── GodRays.tsx             # Raios volumétricos (Ascension)
│   │   │   └── RealityBackground.tsx   # Wrapper condicional
│   │   │
│   │   ├── 📂 effects/                 # ✨ NOVO - Reality Codex Effects
│   │   │   ├── Scanlines.tsx           # Efeito CRT (Military)
│   │   │   ├── BreathingWrapper.tsx    # Animação pulsante (Neural)
│   │   │   └── ConditionalScanlines.tsx # Client wrapper
│   │   │
│   │   ├── 📂 ui/                      # Componentes UI
│   │   │   ├── RealityCard.tsx         # ✨ NOVO - Card adaptativo por realidade
│   │   │   ├── RealityGlitch.tsx       # Efeito de transição
│   │   │   ├── ThemeSwitcher.tsx       # Seletor de realidades (⚙️)
│   │   │   ├── Button.tsx
│   │   │   ├── Card.tsx
│   │   │   └── ...
│   │   │
│   │   ├── 📂 layout/                  # Componentes de layout
│   │   │   ├── Sidebar.tsx
│   │   │   ├── MobileMenu.tsx
│   │   │   └── QuantumBackground.tsx   # (Substituído por RealityBackground)
│   │   │
│   │   ├── 📂 quantum/                 # Componentes específicos
│   │   │   ├── NeuralGraph.tsx         # Neural Nexus
│   │   │   ├── MatrixTerminal.tsx      # Matrix Terminal
│   │   │   └── ...
│   │   │
│   │   ├── AgentCard.tsx               # Card de agente
│   │   ├── MegaCounter.tsx             # Contador de métricas
│   │   ├── OrionCopilot.tsx            # Chat AI
│   │   └── ...
│   │
│   ├── 📂 contexts/                    # React Contexts
│   │   ├── ThemeContext.tsx            # ✨ ENHANCED - Reality support + useReality hook
│   │   ├── AuthContext.tsx
│   │   ├── GamificationProvider.tsx
│   │   └── ToastProvider.tsx
│   │
│   ├── 📂 types/                       # ✨ NOVO - TypeScript Types
│   │   └── reality.ts                  # Sistema completo de tipos Reality Codex
│   │
│   ├── 📂 lib/                         # Utilitários
│   │   ├── store.ts                    # Zustand store
│   │   ├── utils.ts                    # Helpers (cn, etc)
│   │   └── supabase.ts                 # Supabase client
│   │
│   └── 📂 hooks/                       # Custom hooks
│       └── ...
│
├── 📂 apresentacao_do_sistema/         # 🎁 PASTA DE APRESENTAÇÃO
│   │
│   ├── 📂 00_DOCUMENTACAO/
│   │   └── VISAO_GERAL_ALSHAM_QUANTUM.md
│   │
│   ├── 📂 01_CORE_LOGIC/
│   │   ├── store.ts
│   │   └── supabase.ts
│   │
│   ├── 📂 02_INTERFACE_VISUAL/
│   │   ├── layout.tsx
│   │   └── globals.css
│   │
│   ├── 📂 03_PAGINAS_PRINCIPAIS/
│   │   ├── dashboard.tsx
│   │   ├── agents.tsx
│   │   ├── nexus.tsx
│   │   ├── matrix.tsx
│   │   ├── evolution.tsx
│   │   ├── value.tsx
│   │   ├── void.tsx
│   │   ├── gamification.tsx
│   │   └── landing.tsx
│   │
│   ├── 📂 04_COMPONENTES_ESPECIAIS/
│   │   ├── NeuralGraph.tsx
│   │   └── MatrixTerminal.tsx
│   │
│   ├── 📂 05_REALITY_CODEX_v13.3/      # ✨✨✨ NOVO - PACOTE COMPLETO
│   │   │
│   │   ├── LEIA_ME_PROGRAMADOR.md      # 📋 Guia de troubleshooting
│   │   │
│   │   ├── reality.ts                  # Sistema de tipos
│   │   ├── ThemeContext.tsx            # Context enhanced
│   │   ├── ThemeSwitcher.tsx           # Seletor de temas
│   │   ├── RealityCard.tsx             # Card adaptativo
│   │   ├── globals.css                 # CSS completo
│   │   ├── tailwind.config.ts          # Config
│   │   ├── layout.tsx                  # Integração
│   │   │
│   │   ├── 📂 backgrounds/             # 6 backgrounds únicos
│   │   │   ├── QuantumParticles.tsx
│   │   │   ├── TacticalGrid.tsx
│   │   │   ├── NeuralPulse.tsx
│   │   │   ├── PremiumNoise.tsx
│   │   │   ├── GodRays.tsx
│   │   │   └── RealityBackground.tsx
│   │   │
│   │   └── 📂 effects/                 # 3 efeitos visuais
│   │       ├── Scanlines.tsx
│   │       ├── BreathingWrapper.tsx
│   │       └── ConditionalScanlines.tsx
│   │
│   └── LEIA_ME.md                      # Guia geral da pasta
│
├── 📂 docs/                            # Documentação
│   ├── ALSHAM_QUANTUM_MASTERPLAN_v13_FINAL.md
│   ├── PLANTA_FINAL_ALSHAM_QUANTUM_FRONTEND_v12_SUPREMO.md
│   └── ...
│
├── 📄 package.json                     # Dependências do projeto
├── 📄 tsconfig.json                    # TypeScript config
├── 📄 tailwind.config.ts               # ✨ ATUALIZADO - Reality utilities
├── 📄 next.config.js                   # Next.js config
├── 📄 .env.local                       # Variáveis de ambiente
├── 📄 .gitignore
└── 📄 README.md
```

---

## 🎯 ARQUIVOS CHAVE DO REALITY CODEX (v13.3)

### Criados/Modificados Hoje:

#### ✨ Novos Arquivos (15):
1. `src/types/reality.ts` - Sistema completo de tipos
2. `src/components/backgrounds/QuantumParticles.tsx`
3. `src/components/backgrounds/TacticalGrid.tsx`
4. `src/components/backgrounds/NeuralPulse.tsx`
5. `src/components/backgrounds/PremiumNoise.tsx`
6. `src/components/backgrounds/GodRays.tsx`
7. `src/components/backgrounds/RealityBackground.tsx`
8. `src/components/effects/Scanlines.tsx`
9. `src/components/effects/BreathingWrapper.tsx`
10. `src/components/effects/ConditionalScanlines.tsx`
11. `src/components/ui/RealityCard.tsx`
12. `apresentacao_do_sistema/05_REALITY_CODEX_v13.3/` (pasta completa)
13. `apresentacao_do_sistema/05_REALITY_CODEX_v13.3/LEIA_ME_PROGRAMADOR.md`

#### 🔄 Arquivos Modificados (4):
1. `src/contexts/ThemeContext.tsx` - Enhanced com useReality()
2. `src/app/globals.css` - Expandido com 5 realidades
3. `tailwind.config.ts` - Utilities de realidade
4. `src/app/layout.tsx` - Integração RealityBackground

---

## 📊 ESTATÍSTICAS DO PROJETO

- **Total de Páginas:** 9 (Dashboard, Agents, Nexus, Matrix, Evolution, Value, Void, Gamification, Landing)
- **Total de Componentes:** 40+
- **Realidades Implementadas:** 5 (Quantum, Military, Neural, Titanium, Ascension)
- **Backgrounds Únicos:** 6
- **Efeitos Visuais:** 3
- **Linhas de Código Adicionadas (hoje):** ~1500+

---

## 🚀 DEPENDÊNCIAS PRINCIPAIS

```json
{
  "next": "16.0.3",
  "react": "^19.0.0",
  "next-themes": "^0.4.4",
  "framer-motion": "^11.0.0",
  "zustand": "^5.0.3",
  "lucide-react": "^0.462.0",
  "tailwindcss": "^3.4.1",
  "three": "^0.170.0",
  "@supabase/supabase-js": "^2.39.0"
}
```

---

## 🎨 AS 5 REALIDADES

### 1. 🧪 QUANTUM LAB (Padrão)
- Background: Partículas interativas
- Fonte: Orbitron
- Cor: Cyan (#00FFC8)

### 2. 🪖 MILITARY OPS
- Background: Grid tático + crosshairs
- Fonte: IBM Plex Mono (UPPERCASE)
- Cor: Amarelo tático (#F4D03F)

### 3. 🧠 NEURAL SINGULARITY
- Background: Rede neural pulsando 60bpm
- Fonte: Orbitron
- Cor: Roxo neon (#D022FF)

### 4. 💼 TITANIUM EXECUTIVE
- Background: Textura de ruído premium
- Fonte: Inter
- Cor: Azul royal (#38BDF8)

### 5. ☀️ LUMINOUS ASCENSION
- Background: Raios volumétricos (god rays)
- Fonte: Cinzel (serif)
- Cor: Dourado (#D97706)

---

## 📝 COMMITS RECENTES

```
6a5d403 - feat: Implement complete Visual Reality Codex v13.3
          - 15+ novos componentes
          - 5 backgrounds únicos
          - Sistema de tipos completo
          - Pasta de apresentação atualizada
```

---

## 🔗 LINKS IMPORTANTES

- **Repositório GitHub:** `Abnadaparte/suna-alsham-automl`
- **Branch:** `main`
- **Pasta de Apresentação:** `frontend/apresentacao_do_sistema/05_REALITY_CODEX_v13.3/`
- **Guia do Programador:** `05_REALITY_CODEX_v13.3/LEIA_ME_PROGRAMADOR.md`

---

**Este documento serve como mapa completo do repositório para análise técnica.** 🗺️
