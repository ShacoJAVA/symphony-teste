# Plano de orquestração — Dinheiro sem Complicação (V2)

## Objetivo

Coordenar a produção de um pequeno e-book educativo para jovens adultos iniciantes em educação financeira. O conteúdo deve cobrir organização financeira, orçamento pessoal, reserva de emergência, dívidas, juros compostos e primeiros passos para investir.

O Orquestrador define o fluxo e os critérios; não pesquisa, redige, revisa nem cria o projeto visual no lugar dos especialistas.

## Fluxo e dependências

| Ordem | Agente | Issue | Entrada / dependência | Entrega principal |
|---|---|---|---|---|
| 1 | Pesquisador | [GH-7](https://github.com/ShacoJAVA/symphony-teste/issues/7) | Nenhuma | Base conceitual, referências confiáveis, lacunas e pontos que exigem atualização em `pesquisa.md` |
| 2 | Redator | [GH-8](https://github.com/ShacoJAVA/symphony-teste/issues/8) | GH-7 | Manuscrito introdutório em `rascunho.md`, seguindo o escopo e a pesquisa |
| 3 | Revisor | [GH-9](https://github.com/ShacoJAVA/symphony-teste/issues/9) | GH-8 | Revisão registrada e manuscrito corrigido em `revisao.md` e `ebook-final.md` |
| Paralelo à redação/revisão | Designer | [GH-10](https://github.com/ShacoJAVA/symphony-teste/issues/10) | GH-7 | Direção visual, elementos necessários e prompts em `direcao-visual.md`; não altera texto editorial |
| 4 | Finalizador | [GH-11](https://github.com/ShacoJAVA/symphony-teste/issues/11) | GH-9 e GH-10 | Pacote final editável em `entrega-final.md`, preservando conteúdo, ressalvas e referências |

As dependências são declaradas nos corpos das issues. O Finalizador só começa quando a revisão editorial e a direção visual estiverem disponíveis. O Designer pode trabalhar em paralelo ao Redator após a pesquisa.

## Critérios de qualidade e limites

- Cobrir os seis tópicos solicitados com linguagem acessível a iniciantes.
- Separar princípios gerais de informação local ou temporal que precise ser confirmada e referenciada.
- Não inventar estatísticas, taxas, regras, fontes ou circunstâncias do leitor.
- Não prometer resultados nem recomendar produtos específicos; sinalizar que decisões dependem de objetivos, prazo e tolerância a risco individuais.
- Preservar fontes e ressalvas ao longo da revisão e finalização.
- Registrar limitações e bloqueios nos artefatos; nenhuma dependência pendente deve ser tratada como concluída por suposição.

## Encerramento do projeto

O Orquestrador acompanha as issues-filhas e verifica a existência dos artefatos esperados antes de considerar o fluxo concluído. O resultado do Orquestrador limita-se a este plano e ao registro das tarefas delegadas.
