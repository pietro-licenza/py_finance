# Como Contribuir

Guia prático para contribuir com o desenvolvimento do Finanpy seguindo os padrões do projeto.

## Antes de começar

Leia, nessa ordem:

1. [overview.md](./overview.md) — entenda o produto.
2. [stack.md](./stack.md) — confira a stack permitida.
3. [code-style.md](./code-style.md) — padrões de código obrigatórios.
4. [architecture.md](./architecture.md) — decisões arquiteturais (CBVs, signals, isolamento).
5. [design-system.md](./design-system.md) — visual obrigatório.

## Organização do trabalho (Sprints)

O desenvolvimento é segmentado em **5 Sprints**, conforme a seção 13 do [PRD.md](../PRD.md):

| Sprint | Foco |
|--------|------|
| 1 | Setup inicial, arquitetura de apps e Custom User. |
| 2 | Frontend base, Design System e telas públicas (auth). |
| 3 | Gestão de contas bancárias e categorias. |
| 4 | Transações, sincronização de saldo e Dashboard. |
| 5 | Refinação, testes automatizados e Dockerização. |

Cada Sprint contém tarefas e subtarefas detalhadas no PRD. Marque o que for sendo entregue.

## Estado atual

A Sprint 1 foi parcialmente iniciada:

- ✅ Projeto Django criado (`core/`).
- ✅ As 5 apps foram criadas (`users`, `profiles`, `accounts`, `categories`, `transactions`) e registradas em `INSTALLED_APPS`.
- ⏳ Configurações de localização, Custom User, signals e CBVs ainda pendentes.

Consulte a seção 13 do PRD para a lista detalhada de subtarefas em aberto.

## Fluxo de contribuição

1. **Identifique a tarefa** na Sprint correspondente do PRD.
2. **Implemente** seguindo os padrões deste diretório `docs/`.
3. **Rode `python manage.py makemigrations` + `migrate`** se houver alterações em models.
4. **Verifique manualmente** o fluxo afetado (cadastro → login → criação → ...).
5. **Audite** o código conforme o checklist abaixo.

## Checklist de qualidade

Antes de considerar uma tarefa concluída:

- [ ] Código em **inglês**, interface em **pt-BR**.
- [ ] **PEP8** sem warnings.
- [ ] **Aspas simples** em todas as strings (Python e HTML), exceto onde a sintaxe exigir.
- [ ] Modelos novos têm `created_at = models.DateTimeField(auto_now_add=True)` e `updated_at = models.DateTimeField(auto_now=True)`.
- [ ] Views novas são **CBVs**.
- [ ] Views autenticadas usam **`LoginRequiredMixin`** e filtram `get_queryset` por `self.request.user`.
- [ ] Lógica de saldo de contas vive em `transactions/signals.py`, **nunca** nas views.
- [ ] HTML usa exclusivamente o **Design System** (cores, gradientes, componentes).
- [ ] Migrações geradas e versionadas.
- [ ] Teste manual ponta-a-ponta no fluxo afetado.

## Convenções de Git (sugeridas)

Como o repositório atual não inclui regras formais de Git, siga estas recomendações:

- Mensagens de commit em **inglês**, no imperativo (`Add user model`, `Fix balance update on delete`).
- Um commit por unidade lógica de mudança.
- Referencie a Sprint/tarefa quando aplicável (`Sprint 1 / Task 1.3: implement custom user model`).

## Áreas fora de escopo até a Sprint 5

Conforme **RNF-005** do PRD:

- 🚫 **Testes automatizados** — só na Sprint 5 (`users/tests.py`, `accounts/tests.py`, `transactions/tests.py`).
- 🚫 **Docker / docker-compose** — só na Sprint 5.

Não invista esforço nesses temas antes da fase de consolidação.

## Em caso de dúvida

- Consulte o **PRD.md** para requisitos e critérios de aceite.
- Confira a documentação específica do tema em `docs/`.
- Se o padrão não estiver coberto aqui, prefira **a opção mais enxuta e nativa do Django** — esse é o espírito do projeto.
