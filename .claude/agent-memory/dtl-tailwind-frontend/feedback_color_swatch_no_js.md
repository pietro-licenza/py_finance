---
name: feedback-color-swatch-no-js
description: When showing a preview of a ColorInput / hex value, render the preview as a separate inline-styled span next to the native input — never wrap the input itself or add JS.
metadata:
  type: feedback
---

For ColorInput fields in a Finanpy form, render a small visual swatch (a `<span>` with `style='background-color: {{ form.color.value|default:'#667eea' }};'`) placed to the LEFT of the `<input type='color'>`. The native picker stays as the interactive control; the swatch gives the user a larger colored block to see. All values come from DTL on initial render — no `<script>` is used.

**Why:** The project rule is "No `<script>` blocks unless strictly necessary for a native interaction." A swatch that needs JS to stay in sync on every `input` event would violate that. Initial value from DTL is enough for create/edit flows because the page reloads on submit.

**How to apply:** Whenever you need to preview a user-pickable color in a form, use the inline-styled-span pattern. The two allowed inline styles in the whole codebase are: (1) the form color preview swatch, and (2) the category delete-confirmation summary swatch. Both are the only acceptable `style='...'` uses because Tailwind cannot read a dynamic hex string.

Related: [[reference-url-namespaces-categories]]
