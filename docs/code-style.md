# Padrões de Código

Estas regras valem para todo código-fonte do Finanpy. Auditoria de conformidade é feita ao final das Sprints.

## Idioma

- **Código-fonte**: Inglês.
  - Nomes de variáveis, classes, funções, models, views, métodos.
  - Comentários internos e docstrings.
  - Mensagens de commit.
  - Nomes de arquivos e migrações.
- **Interface do usuário (UI)**: Português Brasileiro (pt-BR).
  - Labels, botões, mensagens de erro/sucesso, placeholders — tudo em pt-BR.
  - Nenhum texto em inglês deve aparecer na interface final.

Essa separação é estrita: o código fala inglês, o produto fala português.

## Estilo (PEP8)

O código deve seguir **estritamente** as diretrizes da [PEP8](https://peps.python.org/pep-0008/). Pontos sensíveis no contexto do Django:

- 4 espaços de indentação (sem tabs).
- Linha máxima de 79 caracteres (ou 99 em casos pontuais).
- Duas linhas em branco entre classes; uma linha entre métodos.
- Imports ordenados: stdlib → third-party → local.

## Aspas

**Use sempre aspas simples (`'`)** para strings em Python e em atributos HTML dentro de templates DTL. Aspas duplas (`"`) somente quando a sintaxe exigir:

- Strings que já contêm `'` no conteúdo.
- Docstrings (convenção do Python usa `"""`).
- JSON literal em Python.

### Exemplos

```python
# ✅ Correto
name = 'Conta Corrente'
INSTALLED_APPS = ['accounts', 'users']
queryset = Account.objects.filter(user=self.request.user)

# ❌ Errado
name = "Conta Corrente"
INSTALLED_APPS = ["accounts", "users"]
```

```html
<!-- ✅ Correto -->
<input type='text' name='email' class='block w-full'>

<!-- ❌ Errado -->
<input type="text" name="email" class="block w-full">
```

## Class Based Views (CBVs)

Use **sempre** CBVs nativas do Django:

- `TemplateView`, `ListView`, `CreateView`, `UpdateView`, `DeleteView`.
- `LoginView`, `LogoutView` para autenticação.

Views baseadas em função (`def view(request)`) **não devem** ser usadas, salvo justificativa documentada.

Combine sempre com `LoginRequiredMixin` em telas privadas e sobrescreva `get_queryset` para filtrar pelo `self.request.user`.

## Models

Toda classe de modelo deve incluir:

```python
created_at = models.DateTimeField(auto_now_add=True)
updated_at = models.DateTimeField(auto_now=True)
```

Sem exceções (regra **RNF-004** do PRD).

## Templates (DTL)

- Herde sempre de `base.html` via `{% extends 'base.html' %}`.
- Use blocos: `{% block content %}{% endblock %}`.
- Atributos HTML com aspas simples.
- Classes Tailwind seguindo o [design-system.md](./design-system.md).
- Não misture paletas de cor fora do Design System.

## Localização

No `core/settings.py`:

```python
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True
```

## Valores monetários

- Coluna `DecimalField(max_digits=12, decimal_places=2)`.
- Exibição com símbolo `R$` (Real brasileiro).
- Cores de status: receita em `text-emerald-400`, despesa em `text-rose-400`.

## O que evitar

- ❌ `print()` deixado em código de produção.
- ❌ `_('texto')` ou `gettext` quando o texto pode ir direto em pt-BR no template (o projeto é monolíngue).
- ❌ Misturar lógica de saldo nas views (use signals em `transactions/signals.py`).
- ❌ Acessar dados de outro usuário (sempre filtrar `get_queryset`).
- ❌ Strings com aspas duplas sem motivo sintático.

## Checklist antes de finalizar uma tarefa

- [ ] Código em inglês, UI em pt-BR.
- [ ] PEP8 sem warnings.
- [ ] Aspas simples em strings Python e atributos HTML.
- [ ] Models novos incluem `created_at` e `updated_at`.
- [ ] Views novas são CBVs.
- [ ] Views privadas usam `LoginRequiredMixin` + `get_queryset` filtrado por usuário.
- [ ] Cores e componentes do Tailwind aderem ao Design System.
