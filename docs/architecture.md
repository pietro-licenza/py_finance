# Arquitetura

Diretrizes arquiteturais do Finanpy. As decisões aqui descritas são vinculantes — qualquer desvio precisa de justificativa explícita.

## Princípio fundamental

> **Use apenas o ecossistema nativo do Django.**

Sem APIs REST isoladas. Sem microsserviços. Sem frameworks JavaScript no front. O Django Full Stack (DTL + CBVs) faz todo o trabalho.

## Padrões obrigatórios

### 1. Class Based Views (CBVs)

Todas as views devem ser **Class Based Views nativas** do Django:

- `TemplateView` — páginas estáticas (landing, dashboard).
- `ListView` — listagens.
- `CreateView`, `UpdateView`, `DeleteView` — operações de CRUD.
- `LoginView`, `LogoutView` — autenticação (nativas).

Views baseadas em função (`def view(request)`) **não devem** ser usadas, exceto em situações excepcionais documentadas.

### 2. Isolamento por usuário

Toda view que lista, edita ou apaga registros pertencentes a um usuário deve:

1. Usar o mixin `LoginRequiredMixin`.
2. Sobrescrever `get_queryset` para filtrar pelo `self.request.user`.

Exemplo conceitual:

```python
class AccountListView(LoginRequiredMixin, ListView):
    model = Account

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)
```

Isso garante que um usuário **nunca** veja ou manipule dados de outro.

### 3. Autenticação por e-mail

- O modelo `users.User` substitui o `username` clássico do Django por `email` como chave única de identificação.
- A configuração `AUTH_USER_MODEL = 'users.User'` deve estar em `settings.py`.
- O fluxo de login só aceita `email + senha`.

### 4. Sincronização de saldos via Signals

A atualização do saldo das contas (`Account.balance`) ao criar/editar/remover uma transação deve viver em **`transactions/signals.py`**, **não** espalhada pelas views.

Sinais escutados:

- `post_save` em `Transaction` — aplica o impacto (somar/subtrair) considerando edições.
- `post_delete` em `Transaction` — reverte o impacto.

O `TransactionsConfig.ready()` registra os sinais. Mesma lógica vale para a criação automática de `Profile` em `profiles/signals.py` via `post_save` do `User`.

### 5. Auditoria temporal

**Toda tabela** criada no projeto deve incluir:

```python
created_at = models.DateTimeField(auto_now_add=True)
updated_at = models.DateTimeField(auto_now=True)
```

Sem exceções.

## Templates (DTL)

- Engine única: **Django Template Language**.
- Layout base: `templates/base.html` define o esqueleto (estrutura HTML, importação do Tailwind, blocos).
- Templates filhos herdam via `{% extends 'base.html' %}` e preenchem `{% block content %}`.
- O bloco `TEMPLATES['DIRS']` do `settings.py` aponta para a pasta `templates/` na raiz.

## Estrutura de URLs

- O `core/urls.py` é o roteador raiz.
- Cada app define seu próprio `urls.py` e é incluída via `include('app.urls')` no `core/urls.py`.
- Configurações de redirecionamento pós-login/logout:
  - `LOGIN_REDIRECT_URL = 'dashboard'`
  - `LOGOUT_REDIRECT_URL = 'landing'`

## Banco de Dados

- **Único:** SQLite, no arquivo `db.sqlite3` na raiz.
- Sem servidor externo. Sem suporte a outros SGBDs.

Detalhes do esquema em [database.md](./database.md).

## O que **não** fazer

- ❌ Criar endpoints JSON/REST separados.
- ❌ Renderizar templates fora do DTL.
- ❌ Calcular saldos diretamente em views (use signals).
- ❌ Usar `username` para login.
- ❌ Criar models sem `created_at` / `updated_at`.
- ❌ Permitir que um usuário acesse dados de outro (sempre filtrar `get_queryset`).
