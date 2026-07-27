# APIs de Execução — Diretor Lá na Chácara

**Regra de ouro:** chaves SEMPRE em variáveis de ambiente. Nunca em código, nunca coladas no chat, nunca commitadas.

Variáveis esperadas: `FAL_KEY`, `IDEOGRAM_API_KEY`, `OPENAI_API_KEY`, `BUFFER_ACCESS_TOKEN`.

Antes de executar, verifique: `python scripts/gerar_imagem.py --check` (mostra quais chaves estão presentes, sem exibir valores).

## 1. Geração de imagem — `scripts/gerar_imagem.py`

```bash
# Ideogram (cards com texto em placa)
python scripts/gerar_imagem.py --provider ideogram --prompt "..." --out card.png

# OpenAI GPT Image (cenas ricas)
python scripts/gerar_imagem.py --provider openai --prompt "..." --out card.png

# fal.ai FLUX (consistência com referências)
python scripts/gerar_imagem.py --provider fal --prompt "..." --refs ref1.png,ref2.png --out card.png
```

Todos geram em 4:5 vertical por padrão (`--aspect 4:5`).

Notas por provedor:
- **Ideogram:** endpoint `https://api.ideogram.ai/generate` (v1) — se receber 404/410, o endpoint pode ter mudado de versão; consulte docs.ideogram.ai e ajuste `IDEOGRAM_URL` no topo do script. Usar `magic_prompt_option: OFF` para respeitar o prompt canônico à risca.
- **OpenAI:** usa `POST /v1/images/generations` com o modelo de imagem mais recente disponível na conta (`gpt-image-1` como fallback). Tamanho 1024x1280 ≈ 4:5.
- **fal.ai:** usa o endpoint queue do modelo FLUX mais recente com suporte a referência. O script está configurado para `fal-ai/flux-2` — se a conta tiver Kontext ou versão mais nova, trocar `FAL_MODEL` no topo do script. `--refs` aceita até 8 imagens do Pacote de Referência.

## 2. Agendamento — `scripts/agendar_buffer.py`

```bash
# Listar perfis conectados (pegar o profile_id do @lanachacara)
python scripts/agendar_buffer.py --list-profiles

# Agendar um post
python scripts/agendar_buffer.py --profile PROFILE_ID \
  --text "legenda completa com hashtags" \
  --media card.png \
  --when "2026-07-12 11:00" --tz America/Sao_Paulo
```

Notas:
- Usa a API clássica do Buffer (`api.bufferapp.com/1/`). Se a conta usar o adaptador próprio do Kraken em vez do token clássico, preferir o adaptador — mesma interface de agendamento, e mantém "Lei de Marca".
- Carrosséis: o Buffer via API aceita mídia única em alguns planos; se o carrossel falhar via API, agendar como rascunho e finalizar no app do Buffer (o script avisa quando isso acontecer).
- SEMPRE mostrar ao criador o Pacote de Publicação e receber "aprovado" antes de agendar.

## 3. Fluxo completo de um dia de produção (modo execução)

1. Ler `references/biblia.md`.
2. Ritual Diário → criador aprova o card.
3. `gerar_imagem.py` com o provedor da regra de roteamento.
4. Mostrar a imagem ao criador → aprovada?
5. `agendar_buffer.py` no slot da grade.
6. Registrar o card no Banco de Cards Prontos (seção 10 da bíblia) — prompt + legenda.
