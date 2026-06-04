---
name: feedback-tailwind-bundle-check
description: Quando computed style é rgba(0,0,0,0) mas a classe Tailwind está no template, pedir rebuild do bundle antes de debug de template
metadata:
  type: feedback
---

Regra: Se o Playwright reportar que um `computed style` de um dot/badge/borda é `rgba(0, 0, 0, 0)` (transparente) mas o `class` attribute contém a utility Tailwind esperada (ex.: `bg-emerald-400`, `bg-slate-700/60`, `w-2.5 h-2.5`), **NÃO** pedir pro frontend mexer no template. Pedir `python manage.py tailwind build` (ou o comando equivalente do projeto) para regenerar o bundle CSS, e re-testar.

**Why:** Em 2026-06-04, durante a QA da Tarefa 3.5 (Sprint 3 — listagem de Categorias), o frontend já tinha entregado o `category_list.html` com todas as classes Tailwind certas. Mas o bundle `theme/static/css/dist/styles.css` (24.007 bytes) tinha sido gerado contra um set de classes que NÃO incluía `bg-emerald-400`, `bg-rose-400`, `w-2.5 h-2.5`, `bg-slate-700/60`, etc. Resultado: classe certa no HTML, zero efeito visual. O sintoma parecia "template errado" mas era "bundle desatualizado". BUG-003 vs BUG-004 ficaram 1 rodada inteira de QA confusos por isso.

**How to apply:** Antes de pedir qualquer modificação em template, executar:
```bash
ls -la theme/static/css/dist/styles.css
grep -c "<utility-name>" theme/static/css/dist/styles.css
```
Se `grep -c` retornar 0 e a classe estiver sendo usada no template, é BUG do tipo "bundle desatualizado" — pedir rebuild. Se retornar ≥1, aí sim vale debug de template/selector. Ver também [[project-state-sprint-3.5-revalidation]] que documenta o caso real.

Casos onde a regra NÃO se aplica:
- O `class` no template está errado (ex.: escreveu `bg-green-400` em vez de `bg-emerald-400`) — isso é bug de digitação, não de bundle.
- O elemento está coberto por outro elemento com z-index maior, dando错觉 de transparência — aí é layout, não cor.
- O bundle foi regenerado, o servidor Django foi reiniciado, e o navegador do tester está com cache agressivo — pedir hard reload (`Ctrl+Shift+R`) ou append de query string `?v=2` no `<link rel="stylesheet">`.
