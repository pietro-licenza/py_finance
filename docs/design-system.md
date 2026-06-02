# Design System

Identidade visual unificada do Finanpy. Todas as telas (públicas e autenticadas) seguem este padrão sem exceção. **Nenhum outro padrão de cor fora deste escopo deve ser misturado** aleatoriamente no HTML.

## Princípios visuais

- **Tema escuro obrigatório** em todas as telas (públicas e autenticadas).
- **Responsividade obrigatória** (mobile-first ou fluida).
- **Gradientes harmônicos** como linguagem de destaque da marca.
- Tipografia sans-serif nativa (`font-sans`), preferindo Inter quando disponível no sistema.

## Stack visual

- **TailwindCSS** carregado de forma simples no `<head>` do `base.html` (sem build próprio).
- **Django Template Language (DTL)** para a estrutura.
- **Aspas simples** em atributos HTML dentro dos templates (alinhado ao padrão do projeto).

## Paleta de cores

### Fundos

| Uso | Classe Tailwind |
|-----|-----------------|
| Fundo geral da aplicação | `bg-slate-900` ou `bg-neutral-950` |
| Superfícies / cards / modais | `bg-slate-800/60` com borda `border border-slate-700/50` |
| Menu lateral fixo | `bg-slate-950` |

### Texto

| Uso | Classe Tailwind |
|-----|-----------------|
| Texto principal | `text-slate-100` ou `text-white` |
| Texto secundário | `text-slate-400` |

### Gradiente primário da marca

Usado em banners, botões principais e destaques:

```
bg-gradient-to-r from-violet-600 via-indigo-600 to-cyan-500
```

### Status financeiro

| Tipo | Texto | Fundo |
|------|-------|-------|
| Entrada / Receita | `text-emerald-400` | `bg-emerald-500/10` |
| Saída / Despesa | `text-rose-400` | `bg-rose-500/10` |

## Tipografia

```html
<h1 class='text-2xl font-bold tracking-tight text-white sm:text-3xl'>Título da Tela</h1>
<p class='mt-2 text-sm text-slate-400'>Subtítulo explicativo com instruções contextuais.</p>
```

## Componentes

### Botão Primário (com gradiente)

```html
<button type='submit' class='inline-flex items-center justify-center px-4 py-2 text-sm font-medium text-white bg-gradient-to-r from-violet-600 to-indigo-600 hover:from-violet-500 hover:to-indigo-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-slate-900 focus:ring-indigo-500 rounded-lg transition-all duration-200 shadow-lg shadow-indigo-600/20'>
    Salvar Registro
</button>
```

### Botão Secundário / Cancelar

```html
<a href='#' class='inline-flex items-center justify-center px-4 py-2 text-sm font-medium text-slate-300 bg-slate-800 hover:bg-slate-700 border border-slate-700 hover:border-slate-600 rounded-lg transition-colors duration-200'>
    Cancelar
</a>
```

### Input + Label

Padrão para todos os campos de texto do sistema:

```html
<div class='space-y-1'>
    <label for='id_field' class='block text-sm font-medium text-slate-300'>Nome do Campo</label>
    <input type='text' id='id_field' name='field_name' required
           class='block w-full px-3 py-2 bg-slate-800/80 border border-slate-700 rounded-lg text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 text-sm transition-colors duration-150'
           placeholder='Ex: Digite a informação aqui...'>
</div>
```

## Layout estrutural (Shell autenticado)

Todas as telas autenticadas compartilham a mesma casca: menu lateral fixo à esquerda + área de conteúdo à direita.

```html
<div class='min-h-screen bg-slate-900 text-slate-100 font-sans antialiased block md:table w-full'>
    <div class='md:table-row w-full'>
        <aside class='w-full md:table-cell md:w-64 bg-slate-950 border-b md:border-b-0 md:border-r border-slate-800 p-6 vertical-align-top'>
            <div class='flex items-center space-x-3 mb-8'>
                <div class='h-8 w-8 rounded-lg bg-gradient-to-tr from-violet-600 to-cyan-500 flex items-center justify-center font-bold text-white tracking-wider'>F</div>
                <span class='text-xl font-black bg-clip-text text-transparent bg-gradient-to-r from-white to-slate-400'>Finanpy</span>
            </div>
            <nav class='space-y-1'>
                <a href='#' class='flex items-center px-3 py-2.5 text-sm font-medium rounded-lg bg-slate-800 text-white transition-colors'>Dashboard</a>
                <a href='#' class='flex items-center px-3 py-2.5 text-sm font-medium rounded-lg text-slate-400 hover:bg-slate-800/50 hover:text-white transition-colors'>Contas</a>
                <a href='#' class='flex items-center px-3 py-2.5 text-sm font-medium rounded-lg text-slate-400 hover:bg-slate-800/50 hover:text-white transition-colors'>Categorias</a>
                <a href='#' class='flex items-center px-3 py-2.5 text-sm font-medium rounded-lg text-slate-400 hover:bg-slate-800/50 hover:text-white transition-colors'>Transações</a>
            </nav>
        </aside>

        <main class='w-full md:table-cell p-6 md:p-8 vertical-align-top'>
            <div class='max-w-7xl mx-auto space-y-6'>
                <!-- {% block content %}{% endblock %} -->
            </div>
        </main>
    </div>
</div>
```

## Diretrizes

- ✅ Sempre usar `bg-slate-900` no fundo das páginas.
- ✅ Usar `text-emerald-400` para receitas e `text-rose-400` para despesas em listagens de transações.
- ✅ Valores monetários sempre em **Real brasileiro** (`R$`).
- ✅ Aspas simples nos atributos HTML dentro dos templates DTL.
- ❌ Não introduzir paletas de cor fora deste documento.
- ❌ Não usar modo claro / tema branco em nenhuma tela.
