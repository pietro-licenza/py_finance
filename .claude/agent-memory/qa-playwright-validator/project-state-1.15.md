---
name: project-state-1.15
description: Estado do Finanpy na sessão QA de 2026-06-03 (Tarefa 1.15 Testes Manuais de Autenticação)
metadata:
  type: project
---

Estado do Finanpy capturado em 2026-06-03 durante a validação QA da Tarefa 1.15 (Testes Manuais de Autenticação).

**Why:** Contexto para próximas sessões — evita refazer o mesmo trabalho de diagnóstico e serve como linha de base antes da próxima sprint.

**How to apply:** Quando o agente QA for acionado de novo, ler este arquivo antes de testar fluxos de auth — Bugs BUG-001 (CSS Tailwind não compilado) e BUG-002 (URL name `dashboard` ausente) já foram registrados e podem ou não estar corrigidos.

**Servidor e ambiente:**
- Django server roda em `http://127.0.0.1:8000/` via `python manage.py runserver`
- Django 6.0.5, Python 3.14.5
- SQLite em `db.sqlite3` (raiz)
- Virtualenv em `.venv/`

**Bugs abertos identificados:**

1. **BUG-001 (Visual/CSS):** O CSS compilado em `/theme/static/css/dist/styles.css` (13943 bytes) NÃO inclui as classes Tailwind efetivamente usadas nos templates. Apenas `bg-slate-900` está presente; `text-4xl`, `font-extrabold`, `from-violet-*`, `px-8`, `font-black`, etc. **não estão no bundle**. Consequência: `<h1>` renderiza em 16px/400 em vez de 4xl/extrabold, CTAs sem padding, ícones SVG em tamanho default. Body bg slate-900 funciona (classe presente). Causa provável: build do Tailwind não escaneou os templates — `tailwind.config.js` aponta para `../../templates/**/*.html` e `../../**/templates/**/*.html` mas o build pode estar stale. Fix: rodar `cd theme/static_src && npm run build`.

2. **BUG-002 (Funcional/Bloqueante):** `HomeView.get` em `users/views.py:71` chama `redirect('dashboard')` para usuários autenticados, mas **nenhum URL com name `dashboard` está registrado** em `core/urls.py` ou `users/urls.py`. Consequência: qualquer signup ou login bem-sucedido redireciona para `/` que dispara `NoReverseMatch: Reverse for 'dashboard' not found`. Não há shell autenticado acessível. Fix: registrar `path('dashboard/', DashboardView.as_view(), name='dashboard')` em `core/urls.py` (ou usar uma view de placeholder até o Sprint 4).

**Funcionalidades validadas que estão OK:**
- Auth por email (não username) — `F-01` atendido pelo AUTH_USER_MODEL e LoginForm
- Validações de signup (email inválido, senha fraca) — pt-BR, Django UserCreationForm
- Validação de login (credenciais inválidas) — mensagens em pt-BR
- Signal `profiles.signals` cria Profile automaticamente no `post_save` de User (Profile id=21 criado em 2026-06-03 17:55:31 para user_id=27)
- Logout via POST funciona e destrói sessão

**User de teste criado na sessão:**
- Email: `teste.qa.1780509125@finanpy.com`
- Senha: `SenhaForte123!`
- id: 27, is_active: True, Profile vinculado (id 21)

**Pendência para sprints seguintes:**
- URL `dashboard` precisa ser criado (provavelmente Sprint 4 ou antes)
- Shell autenticado (`templates/base.html` com sidebar) — também depende do dashboard
- Build do CSS do Tailwind precisa ser refeito
