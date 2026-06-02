# Agentes — Time de Desenvolvimento Finanpy

Esta pasta concentra os **agentes de IA** especialistas para produzir e validar o código do Finanpy. Cada agente cobre uma função clara no ciclo de desenvolvimento e segue as regras do `PRD.md` e da pasta `docs/`.

Os agentes que geram código (`django-backend`, `dtl-tailwind-frontend`, `db-schema`) **devem** consultar a documentação atualizada das tecnologias via **Context7 MCP** antes de escrever. O agente de QA (`qa-playwright`) **deve** validar o sistema em execução via **Playwright MCP**.

## Índice

| Agente | Arquivo | Função |
|--------|---------|--------|
| Django Backend Specialist | [django-backend.md](./django-backend.md) | Implementa models, CBVs, signals, autenticação por e-mail, URLs e settings. |
| DTL + TailwindCSS Frontend | [dtl-tailwind-frontend.md](./dtl-tailwind-frontend.md) | Constrói templates DTL e a UI dark com TailwindCSS aderente ao Design System. |
| Database & Migrations | [db-schema.md](./db-schema.md) | Modela schemas, escreve migrações Django, otimiza queries e garante integridade. |
| QA / Tester (Playwright) | [qa-playwright.md](./qa-playwright.md) | Valida fluxos e o Design System rodando a aplicação via Playwright MCP. |
| Code Reviewer | [code-reviewer.md](./code-reviewer.md) | Audita diffs e PRs cruzando o código com os padrões de `docs/` e do PRD. |

## Quando usar cada um

| Situação | Agente |
|----------|--------|
| Criar Custom User Model, signals, CBVs, forms, URLs ou ajustar `settings.py`. | `django-backend` |
| Construir / refatorar `base.html`, telas públicas, dashboard, listagens, formulários, parciais HTML. | `dtl-tailwind-frontend` |
| Definir/alterar models, gerar migrações, escrever agregações complexas, garantir integridade financeira no schema. | `db-schema` |
| Validar manualmente fluxos ponta-a-ponta, conferir saldos, conformidade visual, responsividade, pt-BR. | `qa-playwright` |
| Revisar PRs antes do merge, auditoria de Sprint, conferir aderência a PEP8 / aspas simples / signals / Design System. | `code-reviewer` |

## Fluxo recomendado por Sprint

A sequência abaixo cobre o ciclo natural de uma tarefa de feature:

1. **`db-schema`** — desenha/atualiza os models e gera as migrações.
2. **`django-backend`** — implementa views, forms, signals, URLs.
3. **`dtl-tailwind-frontend`** — entrega os templates conforme o Design System.
4. **`qa-playwright`** — valida o resultado no navegador (funcional + visual).
5. **`code-reviewer`** — revisa o diff antes do merge.

Em correções pontuais, pule etapas que não se aplicam (ex: fix de template envolve apenas `dtl-tailwind-frontend` → `qa-playwright` → `code-reviewer`).

## Uso obrigatório de MCP servers

| Agente | MCP server | Para quê |
|--------|------------|----------|
| `django-backend` | `context7` | Sintaxe atualizada de Django 6.0.x (AbstractUser, CBVs, signals, mixins, forms). |
| `dtl-tailwind-frontend` | `context7` | Utilitários atualizados do TailwindCSS e tags/filtros do DTL. |
| `db-schema` | `context7` | Parâmetros atualizados de `DecimalField`, `ForeignKey`, `Constraint`, `RunPython`, agregações. |
| `qa-playwright` | `playwright` | Automação do browser para executar fluxos e capturar evidências. |
| `code-reviewer` | — (opcional `context7` em caso de dúvida) | Cruza o diff com as regras escritas em `docs/` e `PRD.md`. |

## Regras vinculantes que todos os agentes respeitam

Estes pontos vêm do `PRD.md` e de `docs/architecture.md` / `docs/code-style.md` / `docs/design-system.md`. **Nenhum agente pode violá-los**:

- Stack **Django Full Stack** com **DTL + TailwindCSS + SQLite**. Sem REST, sem SPA, sem outro SGBD.
- **CBVs apenas**, com `LoginRequiredMixin` e `get_queryset` filtrado por usuário em telas privadas.
- **Custom User por e-mail** (`users.User`).
- **Saldo de `Account`** mutado exclusivamente em `transactions/signals.py`.
- **Audit fields** (`created_at`, `updated_at`) em todo model.
- **Código em inglês**, **UI em pt-BR**.
- **Aspas simples** em strings Python e atributos HTML.
- **PEP8** estrito.
- **Tema escuro** e paleta fixa do Design System em toda interface.

## Referências cruzadas

- `PRD.md` — fonte da verdade do produto.
- `docs/README.md` — índice da documentação técnica.
- `CLAUDE.md` — orientações curtas para instâncias de Claude Code trabalhando neste repo.
