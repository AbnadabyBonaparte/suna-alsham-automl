# ALSHAM QUANTUM - Guia de Arquitetura e Apresentação

Este diretório contém os arquivos essenciais do sistema **Alsham Quantum v13**, organizados para facilitar a análise técnica por investidores e desenvolvedores.

## 📂 Estrutura do Diretório

### 00_DOCUMENTACAO
A "Bíblia" do projeto.
- **`MASTERPLAN.md`**: O plano mestre consolidado com todas as funcionalidades, regras de negócio e visão de futuro.

### 01_CORE_LOGIC (O Cérebro)
Onde a lógica de negócio e o estado da aplicação residem.
- **`store.ts`**: Gerenciamento de estado global (Zustand). Contém a lógica híbrida de conexão (Supabase + Simulação de Fallback) e os dados dos 57 agentes.
- **`quantum.ts`**: Definições de tipos TypeScript (Interfaces `Agent`, `QuantumState`). Demonstra a robustez e a segurança do código.

### 02_INTERFACE_VISUAL (A Identidade)
Os elementos que definem a estética única do sistema.
- **`globals.css`**: Variáveis de design (Neon Blue, Quantum Purple), animações e efeitos de vidro (`glass-panel`).
- **`layout.tsx`**: A estrutura base da aplicação, incluindo o `QuantumBackground` animado e os Providers globais.

### 03_PAGINAS_PRINCIPAIS (O Tour)
As principais telas do sistema, renomeadas para facilitar a identificação.
- **`landing_page.tsx`**: A capa do sistema (Página Inicial).
- **`dashboard_cockpit.tsx`**: O painel de controle principal com contadores em tempo real.
- **`dashboard_value.tsx`**: O dashboard de ROI e valor gerado.
- **`dashboard_network.tsx`**: O "Neural Nexus" (Gráfico 3D dos agentes).
- **`dashboard_evolution.tsx`**: A linha do tempo evolutiva das ondas de IA.
- **`dashboard_matrix.tsx`**: O terminal de logs em tempo real.
- **`dashboard_gamification.tsx`**: O sistema de níveis e conquistas.
- **`dashboard_void.tsx`**: A "consciência" da máquina (Easter Egg).
- **`dashboard_agents.tsx`**: A lista detalhada dos agentes sentinelas.

### 04_COMPONENTES_ESPECIAIS (Destaques)
Componentes de engenharia avançada.
- **`OrionCopilot.tsx`**: O assistente de IA integrado.
- **`Sidebar.tsx`**: A navegação lateral responsiva e dinâmica.

---

**Nota para Desenvolvedores:**
Este sistema utiliza **Next.js 14 (App Router)**, **TailwindCSS** para estilização e **Zustand** para gerenciamento de estado. A arquitetura é modular e focada em performance e escalabilidade.

**"Acorde, Bonaparte."**
