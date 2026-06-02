# Setup do Ambiente Local

Guia para preparar o ambiente de desenvolvimento e rodar o Finanpy localmente.

## Pré-requisitos

- **Python** instalado (compatível com Django 6.0.5).
- **pip** disponível.
- Terminal com suporte a `python -m venv`.

## 1. Clonar / acessar o projeto

```bash
cd /caminho/para/Finanpy
```

## 2. Criar e ativar o ambiente virtual

O projeto já contém um diretório `.venv/`. Para criar do zero:

```bash
python -m venv .venv
```

Ativar:

```bash
# macOS / Linux
source .venv/bin/activate

# Windows (PowerShell)
.venv\Scripts\Activate.ps1
```

## 3. Instalar dependências

```bash
pip install -r requirements.txt
```

Pacotes instalados:

```
asgiref==3.11.1
Django==6.0.5
sqlparse==0.5.5
```

## 4. Aplicar migrações

```bash
python manage.py migrate
```

O banco `db.sqlite3` é criado/atualizado na raiz do projeto.

## 5. Criar um superusuário (opcional)

Para acessar o admin do Django:

```bash
python manage.py createsuperuser
```

## 6. Rodar o servidor de desenvolvimento

```bash
python manage.py runserver
```

A aplicação fica disponível em `http://127.0.0.1:8000/`.

## Estrutura do `settings.py`

O módulo de configurações principal vive em `core/settings.py`. Pontos relevantes:

- `DEBUG = True` (apenas para desenvolvimento).
- `DATABASES['default']` aponta para `BASE_DIR / 'db.sqlite3'`.
- `INSTALLED_APPS` inclui as 5 apps do projeto: `accounts`, `categories`, `profiles`, `transactions`, `users`.

> **Atenção:** o `SECRET_KEY` exposto no `settings.py` é apenas para desenvolvimento. Em qualquer cenário de produção ele deve ser substituído e mantido em segredo.

## Comandos úteis do Django

```bash
python manage.py makemigrations   # Gera migrações a partir das alterações em models.py
python manage.py migrate          # Aplica migrações pendentes
python manage.py shell            # Abre o shell interativo do Django
python manage.py runserver        # Inicia o servidor de dev
```
