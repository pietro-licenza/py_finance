# Visão Geral

## O que é o Finanpy

O **Finanpy** é um sistema full-stack de gestão de finanças pessoais desenvolvido em Python com o framework Django. Ele centraliza, em uma única plataforma, o controle de:

- Contas bancárias do usuário (corrente, poupança, dinheiro).
- Categorias customizadas de entrada e saída.
- Lançamentos financeiros (transações) com atualização automática de saldo.

O sistema possui uma **área pública institucional** (landing page, cadastro e login) e uma **área autenticada** onde a gestão financeira acontece.

## Propósito

Democratizar e simplificar a organização financeira pessoal por meio de uma ferramenta ágil, visualmente atraente e direta. O projeto também serve como modelo de **desenvolvimento limpo**, mostrando que é possível construir aplicações completas, seguras e escaláveis usando apenas a stack nativa do Django, sem dependências desnecessárias ou arquiteturas infladas.

## Público-Alvo

- Pessoas que buscam uma ferramenta minimalista de controle de gastos diários.
- Usuários que preferem interfaces escuras (*dark mode*), modernas e responsivas.
- Quem deseja categorizar gastos e receitas para entender para onde o dinheiro está indo.

## Princípios do Produto

1. **Simplicidade arquitetural** — apenas a stack padrão do Django (SQLite, DTL, CBVs). Sem APIs REST isoladas, sem microsserviços.
2. **Identidade visual unificada** — Design System coeso com TailwindCSS, ambiente escuro e gradientes harmônicos.
3. **Autenticação por e-mail** — substitui o `username` padrão do Django pelo `email` como chave de identificação.
4. **Entrega incremental** — desenvolvimento em Sprints; testes automatizados e containerização ficam para as fases finais.

## Idioma

- **Interface (UI)**: Português Brasileiro (pt-BR).
- **Código-fonte** (nomes de variáveis, classes, models, views, migrações, comentários, commits): Inglês.

Veja [code-style.md](./code-style.md) para detalhes sobre essa separação.
