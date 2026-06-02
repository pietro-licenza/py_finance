# Apps Django

Referência das cinco apps que compõem o domínio do Finanpy. Cada app tem uma responsabilidade única e isolada.

> **Estado atual:** as cinco apps foram criadas e registradas em `INSTALLED_APPS`, mas a maior parte de seus modelos/views ainda não foi implementada (o projeto está na Sprint 1). Este documento descreve a **responsabilidade de cada app** conforme o PRD, para guiar a implementação.

---

## `users`

**Responsabilidade:** Modelo de usuário customizado autenticado por **e-mail** (não por `username`).

- Classe `User` herda de `AbstractUser`.
- Campo `username` removido (`username = None`).
- Campo `email = models.EmailField(unique=True)` é o identificador único.
- `USERNAME_FIELD = 'email'`, `REQUIRED_FIELDS = []`.
- `UserManager` customizado herdando de `BaseUserManager`, sobrescrevendo `create_user` e `create_superuser`.
- Campos de auditoria obrigatórios: `created_at`, `updated_at`.
- O `settings.py` deve declarar `AUTH_USER_MODEL = 'users.User'`.

Arquivos: `users/models.py`, `users/admin.py`, `users/apps.py`.

---

## `profiles`

**Responsabilidade:** Perfil estendido do usuário, separando dados pessoais da lógica de autenticação.

- Classe `Profile` com `OneToOneField` para o `User` (`on_delete=models.CASCADE`).
- Campos: `first_name`, `last_name`.
- Campos de auditoria: `created_at`, `updated_at`.
- Um `signals.py` escuta o `post_save` do `User` e cria automaticamente o `Profile` correspondente.
- O `ProfilesConfig.ready()` em `profiles/apps.py` importa os sinais.

Arquivos: `profiles/models.py`, `profiles/signals.py`, `profiles/apps.py`.

---

## `accounts`

**Responsabilidade:** Contas bancárias do usuário (carteira, banco, investimentos…).

- Classe `Account` com `ForeignKey` para o usuário dono.
- Campos:
  - `name` — `CharField(max_length=100)`.
  - `account_type` — `CharField(max_length=50)` (ex: `checking`, `savings`, `cash`).
  - `balance` — `DecimalField(max_digits=12, decimal_places=2, default=0.00)`.
  - `created_at`, `updated_at`.
- CRUD completo via CBVs: `AccountListView`, `AccountCreateView`, `AccountUpdateView`, `AccountDeleteView`.
- Todas as views usam `LoginRequiredMixin` e sobrescrevem `get_queryset` para retornar apenas as contas do `self.request.user`.

Arquivos: `accounts/models.py`, `accounts/views.py`, `accounts/admin.py`.

---

## `categories`

**Responsabilidade:** Categorias customizadas para classificar transações como receita ou despesa.

- Classe `Category` com `ForeignKey` para o usuário dono.
- Campos:
  - `name` — `CharField(max_length=100)`.
  - `transaction_type` — `CharField(max_length=20)` (`income` ou `expense`).
  - `created_at`, `updated_at`.
- CRUD completo via CBVs: `CategoryListView`, `CategoryCreateView`, `CategoryUpdateView`, `CategoryDeleteView`.
- Filtragem por usuário no `get_queryset`.

Arquivos: `categories/models.py`, `categories/views.py`, `categories/admin.py`.

---

## `transactions`

**Responsabilidade:** Lançamentos financeiros e sincronização automática do saldo das contas.

- Classe `Transaction` com:
  - `ForeignKey` para `Account` (conta vinculada).
  - `ForeignKey` para `Category` (categoria vinculada).
  - `description` — `CharField(max_length=255)`.
  - `amount` — `DecimalField(max_digits=12, decimal_places=2)`.
  - `transaction_type` — `CharField(max_length=20)` (`income` ou `expense`).
  - `date` — `DateField()`.
  - `created_at`, `updated_at`.
- CRUD completo via CBVs: `TransactionListView`, `TransactionCreateView`, `TransactionUpdateView`, `TransactionDeleteView`.
- Dropdowns de seleção (`Account`, `Category`) filtrados pelo usuário logado.
- **Sincronização de saldo via signals** (`transactions/signals.py`):
  - `post_save`: soma ou subtrai o valor no `Account.balance` conforme `transaction_type`.
  - Em edições, reverte o impacto anterior antes de aplicar o novo.
  - `post_delete`: reverte o impacto da transação removida.
- `TransactionsConfig.ready()` em `transactions/apps.py` importa os sinais.

Arquivos: `transactions/models.py`, `transactions/signals.py`, `transactions/views.py`, `transactions/apps.py`.

---

## Registro em `INSTALLED_APPS`

As cinco apps já estão registradas em `core/settings.py`:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts',
    'categories',
    'profiles',
    'transactions',
    'users',
]
```
