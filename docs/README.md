# Documentação Finanpy

Bem-vindo(a) à documentação interna do **Finanpy** — sistema full-stack de gestão de finanças pessoais construído em Python + Django.

Esta pasta concentra os guidelines, padrões e referências técnicas necessários para entender e contribuir com o projeto. Cada arquivo cobre um tema específico para que seja fácil consultar apenas o que importa.

> Para a especificação completa do produto, consulte o [PRD.md](../PRD.md) na raiz do repositório.

## Índice

| # | Documento | Descrição |
|---|-----------|-----------|
| 1 | [overview.md](./overview.md) | Visão geral, propósito e público-alvo do produto. |
| 2 | [stack.md](./stack.md) | Stack tecnológica oficial e dependências. |
| 3 | [setup.md](./setup.md) | Como preparar o ambiente local e rodar a aplicação. |
| 4 | [structure.md](./structure.md) | Estrutura de diretórios do projeto. |
| 5 | [apps.md](./apps.md) | Referência das apps Django existentes. |
| 6 | [architecture.md](./architecture.md) | Decisões arquiteturais (CBVs, signals, DTL). |
| 7 | [database.md](./database.md) | Esquema de banco de dados e convenções. |
| 8 | [design-system.md](./design-system.md) | Design system: paleta, tipografia e componentes Tailwind. |
| 9 | [code-style.md](./code-style.md) | Padrões de código (PEP8, aspas simples, idiomas). |
| 10 | [contributing.md](./contributing.md) | Fluxo de contribuição e organização em Sprints. |

## Como ler esta documentação

- **Novo no projeto?** Comece por `overview.md` → `stack.md` → `setup.md`.
- **Vai contribuir com código?** Leia `code-style.md`, `architecture.md` e `contributing.md`.
- **Vai mexer no front-end?** Veja `design-system.md`.
- **Vai criar/alterar models?** Consulte `database.md` e `apps.md`.
