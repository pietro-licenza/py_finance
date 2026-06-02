# Stack Tecnológica

O Finanpy é construído estritamente sobre o ecossistema nativo do Django. Nada de APIs separadas, nada de frameworks JavaScript no front-end.

## Stack Oficial

| Camada | Tecnologia |
|--------|-----------|
| Linguagem | **Python** |
| Framework Web | **Django** (Full Stack) |
| Engine de Templates | **Django Template Language (DTL)** |
| Estilização | **TailwindCSS** (utilitário, sem build próprio) |
| Banco de Dados | **SQLite** (arquivo único, nativo) |

## Dependências instaladas

Conforme `requirements.txt`:

```
asgiref==3.11.1
Django==6.0.5
sqlparse==0.5.5
```

Nenhuma dependência adicional deve ser introduzida sem justificativa clara — o projeto preza por **enxutismo**.

## O que **não** entra na stack

Estas tecnologias estão deliberadamente fora do escopo:

- ❌ Django REST Framework ou qualquer outra camada de API.
- ❌ React, Vue, Angular ou frameworks JS de SPA.
- ❌ PostgreSQL, MySQL ou qualquer outro SGBD (somente SQLite).
- ❌ Build tools de front-end (Webpack, Vite). O Tailwind é carregado de forma simples.
- ❌ Celery, Redis, filas de tarefas.
- ❌ Docker (planejado apenas para a Sprint final).

## Versionamento de Python

O projeto usa um ambiente virtual local (`.venv/`). Use uma versão compatível com Django 6.0.x.

## Próximas adições previstas (Sprints finais)

Conforme PRD seção 13 (Sprint 5):

- Testes automatizados nativos (`python manage.py test`).
- Docker + `docker-compose.yml` para subir o serviço web.

Essas adições só ocorrerão na fase de consolidação do MVP.
