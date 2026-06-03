---
name: project-state-1.15-revalidation
description: Revalidação QA da Tarefa 1.15 em 2026-06-03 após correção dos bugs BUG-001 e BUG-002
metadata:
  type: project
---

Estado capturado em 2026-06-03 durante a revalidação QA da Tarefa 1.15 (Testes Manuais de Autenticação) — rodada feita após o `django-backend-specialist` corrigir BUG-001 (CSS) e BUG-002 (URL dashboard).

**Why:** Confirmar que os dois bugs bloqueantes foram realmente resolvidos e que a Tarefa 1.15 pode ser marcada como concluída. Linha de base para próximos sprints (Sprint 4 = dashboard completo com sidebar, contas, categorias).

**How to apply:** Antes de testar fluxos de auth em sessões futuras, ler [[project-state-1.15]] e este arquivo. Se 1.15 estiver marcada concluída, partir para [[project-state-sprint4]] ou similar.

## Resultado da revalidação 1.15

**Placar: 12/12 PASS** — Tarefa 1.15 PODE ser marcada como concluída.

Cenários validados (todos passaram):
- 1.15.1 — `curl http://127.0.0.1:8000/` retorna 200
- 1.15.2 — Landing com hero gradient violet→indigo→cyan, h1 60px font-extrabold, botões com `px-8 py-3.5`, gradient `from-violet-600 to-indigo-600`
- 1.15.3 — `/auth/signup/` renderiza card "Criar Conta" com form
- 1.15.4 — Email inválido (`invalid-email`) → "Informe um endereço de email válido." em pt-BR
- 1.15.5 — Senha fraca (`123`) → 4 mensagens de validação em pt-BR
- 1.15.6 — Cadastro válido com `qa.revalida.1780509998@finanpy.com / SenhaForte123!`
- 1.15.7 — Redirect pós-signup → `/dashboard/` (sem NoReverseMatch — BUG-002 resolvido)
- 1.15.8 — Logout via botão "Sair" no dashboard → redirect para `/`
- 1.15.9 — Login inválido → "Credenciais inválidas. Verifique e tente novamente." + "E-mail ou senha inválidos." (django messages + form)
- 1.15.10 — Login válido → redirect `/dashboard/`
- 1.15.11 — `/` autenticado → redirect `/dashboard/`
- 1.15.12 — Profile auto-criado: user id=29 → Profile id=23

Extras validados:
- F-01 — Login com `username_qualquer` rejeitado (campo é "E-mail" e exige formato válido)
- Auth pages redirecionam para `/dashboard/` quando logado (`/auth/login/` e `/auth/signup/`)

## BUG-001 e BUG-002 — status final

Ambos **RESOLVIDOS**:
- BUG-001: `theme/static/css/dist/styles.css` agora tem 24.007 bytes (era 13.943) e contém `from-violet-600`, `text-4xl`, `font-extrabold`, `px-8`, `bg-clip-text`, `from-indigo-600`, `to-cyan-500`, etc. O CSS é aplicado corretamente: h1 computa 60px font-weight 800, gradient text-clip ativo.
- BUG-002: `DashboardView(LoginRequiredMixin, TemplateView)` em `users/views.py:86`, template `templates/dashboard.html` existe, URL `path('dashboard/', users_views.DashboardView.as_view(), name='dashboard')` em `core/urls.py:34`.

## User de teste da revalidação (deixado no DB)

- Email: `qa.revalida.1780509998@finanpy.com`
- Senha: `SenhaForte123!`
- user id: 29
- Profile id: 23 (auto-criado via signal)

## Pendência para sprints seguintes (inalterada)

- Sprint 4: dashboard completo (`templates/base.html` com sidebar) — Sprint 1 entregou apenas placeholder
- F-04, F-05, F-06, F-07, F-08 — dependem de models Account/Transaction com signals de balance
- Sprint 5: testes automatizados em `tests.py`
