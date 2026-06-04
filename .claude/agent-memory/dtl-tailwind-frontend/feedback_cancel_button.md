---
name: cancel-button-as-anchor
description: In Finanpy CRUD forms, render the Cancelar button as an <a> tag styled as a secondary button, not a <button type='button'>
metadata:
  type: feedback
---

For any "Cancelar" affordance inside a Finanpy form template, render it as an `<a href='{% url "app:list" %}'>` styled with the secondary-button Tailwind classes (`bg-slate-700/60 hover:bg-slate-700 border border-slate-600 hover:border-slate-500 rounded-lg text-slate-200 font-medium`), not as a `<button type='button'>`.

**Why:** An anchor (a) is the most idiomatic DTL pattern for "abandon this form and go back to the list". It works without any JavaScript, the browser's right-click → "Open in new tab" affordance behaves correctly, and the styling is identical to a button when the right Tailwind utilities are applied. Using `<button type='button'>` would require JS to navigate, and `<button type='reset'>` would clear the form (not what the user wants). The pattern is explicit in the project rules: "the cleanest pattern in DTL is to use an `<a>` styled as a secondary button."

**How to apply:** Apply to every CRUD form template (account_form, category_form, transaction_form). Wrap both actions in `<div class='pt-4 flex flex-col-reverse gap-3 sm:flex-row sm:items-center sm:justify-end'>` so the primary "Salvar" button is on the right and Cancelar is on the left on desktop, and they stack with Salvar below on mobile (reversed order so Salvar is still the prominent action). On mobile, `flex-col-reverse` puts Cancelar above Salvar which is the conventional pattern for destructive/secondary actions.
