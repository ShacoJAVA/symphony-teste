---
tracker:
  kind: github
  provider:
    repo: "ShacoJAVA/symphony-teste"
    token: $GITHUB_TOKEN

  active_states:
    - open

  terminal_states:
    - closed

polling:
  interval_ms: 5000

workspace:
  root: ~/code/symphony-workspaces

hooks:
  after_create: |
    git clone https://github.com/ShacoJAVA/symphony-teste.git .

agent:
  max_concurrent_agents: 1
  max_turns: 5

codex:
  command: codex app-server
---

Você está trabalhando na issue {{ issue.identifier }}.

Título:
{{ issue.title }}

Descrição:
{{ issue.description }}

Regras:

1. Leia a issue cuidadosamente.
2. Analise os arquivos existentes antes de modificar qualquer coisa.
3. Faça apenas as mudanças necessárias para resolver a tarefa.
4. Evite alterações fora do escopo.
5. Verifique o resultado antes de terminar.
6. Ao finalizar, explique resumidamente o que foi alterado.
