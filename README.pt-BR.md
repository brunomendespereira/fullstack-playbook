# fullstack-playbook

**Uma Agent Skill que toca o seu produto como uma empresa de software, da ideia ao lançamento, com qualquer agente de código.** Uma skill só para vibe coding e agentic engineering: briefing, design, arquitetura, plano, testes primeiro, código, revisão, QA e lançamento, com princípios de engenharia universais e as tarefas do projeto guardadas no próprio repositório. Funciona no Claude Code e em outros agentes que leem o padrão [Agent Skills](https://agentskills.io).

[English](README.md) · [Licença: MIT](LICENSE) · [Créditos](CREDITS.md)

⭐ **Se ela ajuda o seu produto, deixe uma estrela no repositório.** É assim que o projeto chega a novas pessoas e contribuidores, e continua sendo mantido.

## Por quê

Agentes de código escrevem rápido e esquecem as regras na mesma velocidade. A saída comum é instalar uma skill para cada assunto (fluxo, testes, design, performance de React, composição, segurança). Logo elas se sobrepõem, se contradizem e enchem o contexto antes de o trabalho começar. As regras do próprio produto acabam espalhadas entre arquivos de instrução, memória do agente e listas de tarefas antigas.

A fullstack-playbook troca essa pilha por uma skill que:

- **carrega sob demanda:** cada pedido (feature, bug, ajuste pequeno, revisão, lançamento, produto novo) lê só os poucos arquivos da sua rota, então uma skill gasta menos contexto que uma pilha de skills especializadas (números abaixo);
- **pergunta antes de agir:** plano curto e ok explícito nos pontos de aprovação, uma pergunta por vez;
- **escreve os testes primeiro,** contra um banco de teste de verdade, trava esses testes enquanto o código é escrito e nunca afrouxa um teste que falha;
- **responde seis perguntas de risco** em toda mudança (duplicados, eventos de fora, endpoints, dados de outros usuários, login e dados pessoais, áreas sensíveis), e cada "sim" liga os princípios e os testes obrigatórios correspondentes;
- **revisa com olhos novos:** textos prontos para revisão de spec, padrões, segurança, interface e revisão final, rodados como subagentes ou na própria sessão, sobre um diff ou como auditoria completa do código;
- **aprende de volta:** uma lição que passa no filtro de contribuição fica marcada na memória do produto e, com o seu ok, vira sugestão (issue ou pull request) para este repositório;
- **guarda projetos e tarefas no repositório,** com um arquivo de estado e uma frase de retomada, para qualquer sessão ou agente continuar o trabalho;
- **transforma regra em checagem:** um `verify.sh` que roda em todo commit e um verificador do caderno.

Ela não cita framework, biblioteca nem fornecedor. Os princípios valem para um app React, uma API em Python ou um jogo de celular; a ferramenta é escolhida por produto, depois de pesquisa, e registrada como decisão.

## Carrega sob demanda: uma skill no lugar de várias

Agent Skills carregam em três passos: a descrição curta fica sempre no contexto, o corpo carrega quando a skill é usada e os arquivos de referência só quando uma etapa precisa deles. A fullstack-playbook foi feita em cima disso:

- **Sempre no contexto:** uma descrição de cerca de 220 tokens.
- **Quando chega um pedido:** o roteador (`SKILL.md`, cerca de 2.000 tokens) manda o pedido para os poucos arquivos da rota dele. Uma feature típica lê cerca de 6.700 tokens no total; um ajuste de texto lê o roteador e um modelo.
- **Nada carrega à toa:** as regras de offline e de IA ficam de fora se o produto não precisa delas, e as de segurança, integridade de dados ou interface só entram quando a mudança mexe nisso.

Compare com manter uma skill por assunto. No produto em que esta skill nasceu, sete skills cobriam fluxo de trabalho, qualidade do frontend, design, performance de React, composição de componentes e desenho de módulos. Só as descrições delas ocupavam cerca de 600 tokens de contexto em todo pedido, e uma mudança de frontend que acionava todas juntas carregava cerca de 15.600 tokens só de corpo das skills, antes de ler qualquer arquivo de referência, com regras que se repetiam e às vezes se contradiziam. Páginas, segurança, dados, testes, revisão e lançamento agora vivem numa skill só, com um conjunto só de regras, e cada pedido paga só pelo que usa.

## Como funciona

Duas partes:

- **A skill é o manual.** A mesma para todo produto.
- **Cada produto tem um caderno,** que a skill cria no primeiro uso e atualiza durante o trabalho:

```
seu-produto/
├── PRODUCT.md                 o que é, para quem, tom de voz
├── DESIGN.md                  tokens e regras de design (produtos com telas)
├── AGENTS.md / CLAUDE.md      um bloco curto que aponta para o caderno
└── docs/playbook/
    ├── context.md             stack, estrutura do código, comandos, git, ambientes, valores, regras do produto
    ├── state.md               o que está acontecendo agora e a frase de retomada
    ├── triggers.md            o que este produto faz em cada momento (fim de etapa, lançamento...)
    ├── memory.md              lições e pegadinhas, datadas
    ├── glossary.md            as palavras do domínio
    ├── decisions/             registros de decisão
    ├── projects/<projeto>/    briefing, plano e um arquivo por tarefa
    ├── verify.sh              o gate que roda antes de cada commit e na CI
    └── tools/                 o verificador do caderno (mantido pela skill)
```

O manual diz o que é certo; o caderno diz como isso vale aqui. Quando os dois discordam, vence a regra do produto no `context.md`.

## Instalação

Instale por produto, dentro do repositório.

**Com a CLI de skills:**

```bash
npx skills add brunomendespereira/fullstack-playbook
```

**À mão:** copie `skills/fullstack-playbook/` para o repositório:

- Claude Code: `.claude/skills/fullstack-playbook/`
- A maioria dos outros agentes que leem Agent Skills: `.agents/skills/fullstack-playbook/` (confira onde o seu agente procura skills)

Os scripts precisam só de Python 3 e de um shell POSIX.

## Atualização

Instale a versão nova do mesmo jeito (rode a CLI de novo ou substitua a pasta). A instalação não mexe no seu caderno.

Cada caderno guarda a versão do playbook que o escreveu (`playbook_version` no `context.md`). No primeiro pedido da sessão seguinte, o agente vê que a skill é mais nova e migra o caderno uma vez: acrescenta os campos novos, atualiza o verificador e abre uma tarefa para o que depende da sua decisão. O que cada versão pede de um caderno que já existe está em `workflow/upgrade.md`.

## Primeiro uso

Abra o agente no repositório e peça qualquer coisa, ou diga "Vamos usar o playbook aqui".

- **Produto que já existe:** ele explora o código primeiro, pergunta só o que o código não responde, uma pergunta por vez e com sugestão de resposta, mostra o caderno como rascunho e grava depois do seu ok. Também mapeia a estrutura real do código (onde cada tipo de coisa mora, imports na direção errada) e transforma em tarefas o que diverge do playbook (sem testes, sem CI, regras em conflito).
- **Produto novo:** num repositório vazio, diga o que quer construir ("um app de agendamento para barbearias"). Ele pergunta os requisitos e as qualidades que mais importam (velocidade, privacidade, custo), pesquisa a stack e a organização do código e registra as duas escolhas, e escreve o `PRODUCT.md` e o `DESIGN.md` antes de qualquer código.

## O que tem dentro

| Pasta | O que guarda |
|---|---|
| `SKILL.md` | O roteador: regras que sempre valem, o início de todo pedido, rotas por pedido e por área |
| `workflow/` | Etapas, onboarding, tarefas e estado, gatilhos, depuração, revisão, revisores, lançamento, atualização |
| `principles/` | Produto, arquitetura, código limpo, integridade de dados, segurança, performance, interface, testes |
| `requirements/` | Lidos só quando o produto precisa: offline-first e recursos de IA |
| `templates/` | Os arquivos do caderno, tarefa, plano, briefing, registro de decisão, relatório de revisão, pull request, `verify.sh` |
| `scripts/` | `init_space.py` (cria o caderno), `check_space.py` (confere), `upgrade_space.py` (migra para uma versão nova), `lock_tests.py` (trava os testes escritos antes) |

Toda regra cita uma fonte pública ou é consenso da indústria: OWASP ASVS e API Security Top 10, WCAG 2.2, Core Web Vitals, *Designing Data-Intensive Applications*, *Release It!*, *A Philosophy of Software Design*, *Refactoring*, Nielsen Norman Group, RFC 9457 e RFC 9110, Conventional Commits, SemVer e outras, listadas no fim de cada arquivo.

A skill é escrita em inglês, para servir a qualquer agente e a qualquer pessoa. O caderno de cada produto é escrito no idioma do produto, e o agente conversa no seu idioma.

## Contribuir

Leia o [CONTRIBUTING.md](CONTRIBUTING.md). Em resumo: uma regra precisa de fonte pública, tem que fazer sentido num produto muito diferente, não cita biblioteca nem fornecedor e não guarda valores de gosto. Rode os testes antes de abrir um pull request:

```bash
python3 -m unittest discover tests
```

## Apoie

Deixe uma estrela, abra uma issue com uma lição que o seu produto ensinou ou mande um pull request (veja o [CONTRIBUTING.md](CONTRIBUTING.md)).

## Créditos e licença

MIT. Partes foram adaptadas de projetos abertos, com crédito no [CREDITS.md](CREDITS.md).
