# Estrutura do Projeto

Layout atual do diretório raiz do Finanpy:

```
Finanpy/
├── .venv/                  # Ambiente virtual Python (não versionado)
├── accounts/               # App: contas bancárias do usuário
├── categories/             # App: categorias de transações
├── core/                   # Projeto Django (settings, urls, wsgi, asgi)
├── docs/                   # Documentação do projeto (você está aqui)
├── profiles/               # App: perfil estendido do usuário
├── transactions/           # App: lançamentos financeiros
├── users/                  # App: modelo de usuário customizado
├── .gitignore
├── PRD.md                  # Documento de Requisitos de Produto
├── db.sqlite3              # Banco SQLite (ignorado pelo git)
├── manage.py               # CLI utilitário do Django
└── requirements.txt        # Dependências Python
```

## Pacote `core/`

É o módulo de configuração do projeto Django (gerado por `django-admin startproject core .`).

```
core/
├── __init__.py
├── asgi.py        # Entry point ASGI
├── settings.py    # Configurações globais (DEBUG, INSTALLED_APPS, DATABASES…)
├── urls.py        # Roteamento raiz do projeto
└── wsgi.py        # Entry point WSGI
```

## Apps Django

O Finanpy é organizado em **5 apps**, cada uma com uma responsabilidade clara:

| App | Responsabilidade |
|-----|-----------------|
| `users` | Modelo de usuário customizado autenticado por e-mail. |
| `profiles` | Perfil estendido do usuário (nome, sobrenome). |
| `accounts` | Contas bancárias do usuário. |
| `categories` | Categorias customizadas de receita/despesa. |
| `transactions` | Lançamentos financeiros e sincronização de saldo. |

Cada app segue o layout padrão do Django:

```
<app>/
├── __init__.py
├── admin.py
├── apps.py
├── migrations/
│   └── __init__.py
├── models.py
├── tests.py
└── views.py
```

> Detalhes específicos sobre cada app estão em [apps.md](./apps.md).

## Convenções de localização

- **Templates globais**: planejados para uma pasta `templates/` na raiz, registrada no bloco `TEMPLATES['DIRS']` do `settings.py` (Sprint 2).
- **Arquivos estáticos**: configurados via `STATIC_URL = 'static/'` em `settings.py`.
- **Banco de dados**: `db.sqlite3` na raiz, definido por `BASE_DIR / 'db.sqlite3'`.

## Diretório `docs/`

Cada arquivo cobre um aspecto do projeto. Veja o [README.md](./README.md) para o índice completo.
