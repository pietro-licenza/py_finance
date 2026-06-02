# Finanpy

Sistema **full-stack pessoal de gestão financeira** construído com Django, DTL e TailwindCSS. Sem REST, sem SPA, sem dependências além das listadas em `requirements.txt`.

## Stack

- **Python 3** + **Django 6.0.5**
- **Django Template Language (DTL)** + **TailwindCSS** (via `django-tailwind`)
- **SQLite** como único banco de dados
- **python-decouple** para carregar configuração do `.env`

## Configuração local

```bash
# 1. Ativar o ambiente virtual
source .venv/bin/activate

# 2. Instalar dependências Python
pip install -r requirements.txt

# 3. Instalar dependências do Tailwind (npm)
python manage.py tailwind install

# 4. Aplicar migrações
python manage.py migrate

# 5. Criar superusuário (opcional)
python manage.py createsuperuser

# 6. Subir o servidor de desenvolvimento
python manage.py runserver
# → http://127.0.0.1:8000/
```

## Variáveis de ambiente

O projeto lê configuração sensível do arquivo `.env` (que está no `.gitignore`):

| Variável       | Obrigatória | Default                | Descrição                                                       |
|----------------|-------------|------------------------|-----------------------------------------------------------------|
| `SECRET_KEY`   | sim         | —                      | Chave criptográfica do Django. Gerar com `get_random_secret_key`.|
| `DEBUG`        | não         | `False`                | `True` em desenvolvimento, `False` em produção.                  |
| `ALLOWED_HOSTS`| não         | `127.0.0.1,localhost`  | Lista CSV de hostnames servidos.                                |
| `NPM_BIN_PATH` | não         | `npm`                  | Caminho do binário `npm` (raramente precisa ajustar).            |

## Estrutura

```
.
├── core/                  # Projeto Django (settings, urls, wsgi, asgi)
├── accounts/              # App de contas bancárias do usuário
├── categories/            # App de categorias (entrada/saída)
├── profiles/              # App de perfil (1:1 com User)
├── transactions/          # App de transações + signals de saldo
├── users/                 # Custom User model (autenticação por e-mail)
├── theme/                 # App gerado pelo django-tailwind
│   ├── static_src/        # Fonte Tailwind (CSS, npm, config)
│   └── templates/         # base.html padrão do Tailwind
├── templates/             # Templates globais (base.html, auth/, accounts/, ...)
├── static/                # Assets estáticos do projeto
├── docs/                  # Documentação técnica
├── agents/                # Especificações dos agentes de IA
├── manage.py
├── requirements.txt
└── .env                   # Configuração local (git-ignored)
```

## Comandos úteis

```bash
# Servidor dev com hot-reload do Tailwind
python manage.py runserver
python manage.py tailwind start   # em outro terminal

# Build do CSS do Tailwind para produção
python manage.py tailwind build

# Migrações
python manage.py makemigrations
python manage.py migrate

# Validação rápida do projeto
python manage.py check
```

## Documentação

- `PRD.md` — especificação completa do produto (requisitos, design system, sprints).
- `docs/` — arquitetura, schema do banco, padrões de código, design system.
- `agents/` — contratos dos agentes de IA usados no desenvolvimento.
- `CLAUDE.md` — orientações para o Claude Code trabalhar neste repositório.

## Licença

Projeto privado. Sem licença pública definida.
