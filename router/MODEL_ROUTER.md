# GALAEM Model Router V1

Este arquivo define como o sistema multiagente escolhe o provedor/modelo adequado para cada tarefa.

## Princípio

O agente define O QUE precisa ser feito.

O Model Router define QUAL capacidade e QUAL provedor devem executar o trabalho.

Não associe permanentemente um agente a um único modelo.

Exemplo:

DESIGNER não significa necessariamente Gemini.
DESIGNER pode solicitar CAPACIDADE: IMAGEM e o Router escolhe o provedor configurado.

---

## CAPACIDADES

### ORQUESTRACAO

Uso:
- decomposição de projetos;
- criação de tarefas;
- definição de dependências;
- acompanhamento do projeto.

Rota padrão:
- provider: openai
- executor: codex

### PESQUISA

Uso:
- pesquisa;
- levantamento de informações;
- referências;
- análise de fontes.

Rota padrão:
- provider: openai
- executor: codex

### TEXTO

Uso:
- redação;
- reescrita;
- documentos;
- roteiros;
- conteúdo de e-books.

Rota padrão:
- provider: openai
- executor: codex

### REVISAO

Uso:
- revisão crítica;
- consistência;
- análise de contradições;
- verificação editorial.

Rota padrão:
- provider: openai
- executor: codex

### IMAGEM

Uso:
- geração de imagens;
- ilustrações;
- capas;
- conceitos visuais.

Rota desejada:
- provider: google
- executor: gemini

Status:
- NAO_CONECTADO

Enquanto o provedor não estiver conectado:
- produza briefing visual;
- produza prompts;
- NÃO afirme que uma imagem foi gerada.

### CODIGO

Uso:
- programação;
- automações;
- páginas;
- aplicações;
- testes.

Rota padrão:
- provider: openai
- executor: codex

### VIDEO

Uso:
- geração de vídeo;
- animações;
- peças audiovisuais.

Rota desejada:
- provider: a_configurar
- executor: a_configurar

Status:
- NAO_CONECTADO

Enquanto não houver provedor:
- produza roteiro;
- storyboard;
- prompts;
- especificações técnicas;
- NÃO afirme que o vídeo foi gerado.

### FINALIZACAO

Uso:
- reunir artefatos;
- validar entregas;
- gerar pacote final;
- preparar formatos de entrega.

Rota padrão:
- provider: openai
- executor: codex

---

## REGRA DE ROTEAMENTO

Toda tarefa multiagente V3 deve declarar:

CAPACIDADE: <capacidade>

Opcionalmente:

PROVIDER_PREFERIDO: <provider>
MODELO_PREFERIDO: <modelo>

Se nenhum provedor específico for solicitado, consulte este arquivo.

Se a capacidade estiver marcada como NAO_CONECTADO:

1. não simule a execução externa;
2. produza os insumos necessários para o futuro executor;
3. registre claramente a limitação;
4. mantenha os artefatos reutilizáveis.

---

## ARQUITETURA ALVO

Projeto
  -> Orquestrador
      -> Model Router
          -> OpenAI / Codex
          -> Google / Gemini
          -> Anthropic / Claude
          -> Gerador de imagens
          -> Gerador de vídeo
          -> outros provedores futuros

O projeto não deve depender diretamente de um provedor.

O projeto solicita uma CAPACIDADE.

O Router decide como essa capacidade será atendida.
