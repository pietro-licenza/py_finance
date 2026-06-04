---
name: project-state-sprint-3.5-revalidation
description: Revalidação QA da Tarefa 3.5 (listagem de categorias) em 2026-06-04 após correção dos bugs BUG-003 e BUG-004
metadata:
  type: project
---

Estado capturado em 2026-06-04 durante a revalidação QA da Tarefa 3.5 (Sprint 3 — listagem de Categorias) — rodada feita após o `dtl-tailwind-frontend` corrigir BUG-003 (CSS bundle Tailwind incompleto) e após limpeza manual da categoria residual (BUG-004) no DB.

**Why:** Confirmar que (a) o rebuild do `styles.css` recolocou todas as utilities Tailwind necessárias para os computed styles funcionarem, e (b) o banco de teste está com o conjunto correto de 7 categorias QA-3.5 (3 INCOME + 4 EXPENSE) para evitar que o usuário A herde dados antigos de outros sprints.

**How to apply:** Antes de testar `/categories/` em sessões futuras, ler [[project-state-1.15-revalidation]] e este arquivo. Se 3.5 estiver marcada concluída, partir para [[project-state-sprint-4]] (CRUD de categorias + transações) ou similar.

## Resultado da revalidação 3.5

**Placar: 5/5 PASS** nos cenários que falharam — Tarefa 3.5 PODE ser marcada como concluída.

Cenários re-validados (todos passaram via computed styles, não só visual):

- **V-02** — Header "Entradas": dot 10x10px com `bg-emerald-400` → `rgb(52, 211, 153)`, h2 `text-emerald-400` → `rgb(52, 211, 153)`, contagem `(3)` em verde. (era 0x0 transparente)
- **V-03** — Header "Saídas": dot 10x10px com `bg-rose-400` → `rgb(251, 113, 133)`, h2 e contagem `(4)` em vermelho. (era 0x0 transparente)
- **V-05** — Dot 8x8px dentro de cada badge com `style="background-color: #0ea5e9"` → renderiza `rgb(14, 165, 233)` em 8x8px. (era 0x0)
- **V-06** — Botões "Editar" (`bg-slate-700/60` = `rgba(51,65,85,0.6)`, `text-slate-200`, ícone 14x14) e "Excluir" (`bg-rose-500/10` = `rgba(244,63,94,0.1)`, `text-rose-300`, ícone 14x14). (bg era 0x0)
- **V-09** — Mobile 375x812: botão "Nova Categoria" agora 343x40 (não 253px), ícone `+` em 16x16px (`w-4 h-4`), header empilha abaixo do botão. (botão era absurdamente alto)

Confirmações extras (anti-regressão):
- F-01 — `/categories/` sem login → `302 → /auth/login/?next=/categories/` (browser e curl)
- F-02 — Login com `qa-admin@finanpy.local` / `TempPass!2026` → autenticado
- F-03 — Page title `Minhas Categorias — Finanpy`, sem NoReverseMatch
- V-01 — 2 seções "Entradas" e "Saídas" renderizam
- V-04 — 7 articles (3+4) — categoria residual "Alimentação (QA Sprint 3.2)" removida
- F-09 — Botão "Sair" no dashboard → redirect para `/` (landing)

## BUG-003 e BUG-004 — status final

Ambos **RESOLVIDOS**:
- BUG-003: `theme/static/css/dist/styles.css` agora tem 29.351 bytes (era 24.007) e contém todas as utilities faltantes: `bg-emerald-400`, `bg-rose-400`, `bg-slate-700/60`, `w-2`, `h-2`, `w-2.5`, `h-2.5`, `w-3.5`, `h-3.5`, `w-4`, `h-4`, `sm:flex-row`, `sm:text-3xl`, `px-2.5`, `py-1.5`, `py-2.5`, `gap-2`, `gap-3`, `shrink-0`, `min-w-0`, `truncate`, `border-dashed`, `focus:ring-indigo-500`. Build via `python manage.py tailwind build`.
- BUG-004: categoria residual deletada do DB. `qa-admin@finanpy.local` agora tem 7 categorias QA-3.5:
  - INCOME: `QA-3.5 Freelance` (#0ea5e9), `QA-3.5 Investimentos` (#f59e0b), `QA-3.5 Salário` (#10b981)
  - EXPENSE: `QA-3.5 Alimentação` (#ef4444), `QA-3.5 Lazer` (#ec4899), `QA-3.5 Moradia` (#06b6d4), `QA-3.5 Transporte` (#a855f7)

## Screenshots capturados (substituem os antigos)

- `/Users/lemon/Desktop/Finanpy/.playwright-mcp/sprint-3.5-category-list-desktop-rerun.png`
- `/Users/lemon/Desktop/Finanpy/.playwright-mcp/sprint-3.5-category-list-mobile-rerun.png`

## Lição operacional (feedback a memorizar)

Quando a QA inicial reporta BUG de "computed style = `rgba(0,0,0,0)`" mas o `class` attribute tem a utility certa, **sempre** pedir pra rodar `python manage.py tailwind build` antes de re-testar. O Playwright em dev do Django não tem problema de cache — o problema é que o bundle CSS servido foi gerado contra um set de classes que não inclui a utility em questão. O sintoma aparece como se a classe não tivesse efeito, mas o template está certo.

**Why:** Quebramos a cabeça debugando template e selector quando o problema era apenas o bundle desatualizado. Perdi ~1 rodada inteira de QA por isso.

**How to apply:** Antes de pedir fix de template, rodar `ls -la theme/static/css/dist/styles.css` e `grep -c <utility> theme/static/css/dist/styles.css` para confirmar se a utility está no bundle. Se não estiver, pedir rebuild antes de qualquer outra ação.

## Pendência para sprints seguintes

- Sprint 4: implementar CRUD de Categorias (3.6 — Create, 3.7 — Update, 3.8 — Delete) usando o mesmo shell
- Sprint 4/5: CRUD de Accounts (mesmo padrão de listagem)
- Sprint 5: CRUD de Transactions + signals de balance
- Sprint 5: testes automatizados em `tests.py`
