# Documento de Requisitos de Produto (PRD) - Finanpy

## 1. Visão Geral
O **Finanpy** é um sistema full-stack de gestão de finanças pessoais desenvolvido em Python e Django. O foco principal do projeto é a simplicidade e a eficiência, evitando qualquer tipo de *over-engineering*. Ele oferece aos usuários uma interface moderna, responsiva, com tema escuro e elementos visuais sofisticados (como gradientes de cores), permitindo o controle completo de suas contas bancárias, categorias personalizadas e lançamentos financeiros (entradas e saídas). Toda a experiência do usuário (UI) é adaptada para o português brasileiro, enquanto o código-fonte segue estritamente padrões internacionais em inglês e as diretrizes de estilo da PEP8, utilizando sempre aspas simples (`'`).

## 2. Sobre o Produto
O Finanpy centraliza o ecossistema financeiro de um indivíduo em uma única plataforma unificada. Utilizando as capacidades nativas do ecossistema Django (Django Template Language e Class-Based Views) combinado com o poder utilitário do TailwindCSS, o produto entrega uma experiência fluida sem a complexidade de frameworks JavaScript modernos (como React ou Vue). O sistema possui uma área pública institucional para atração de novos usuários e uma área autenticada robusta onde ocorre a gestão financeira propriamente dita.

## 3. Propósito
O propósito do Finanpy é democratizar e simplificar a organização financeira pessoal através de uma ferramenta ágil, visualmente atraente e extremamente direta. O projeto serve como um modelo de desenvolvimento limpo, priorizando recursos nativos do Django e provando que aplicações completas, seguras e escaláveis podem ser construídas de forma enxuta, sem dependências desnecessárias ou arquiteturas infladas.

## 4. Público-Alvo
* Indivíduos que buscam uma ferramenta minimalista e direta para controle de gastos diários, sem excesso de relatórios complexos ou integrações bancárias automáticas confusas.
* Usuários entusiastas de tecnologia e design que preferem interfaces escuras (*dark mode*) modernas, fluidas e otimizadas para dispositivos móveis e desktops.
* Pessoas que necessitam categorizar seus gastos e receitas de forma customizada para entender para onde seu dinheiro está indo no final do mês.

## 5. Objetivos
* **Simplicidade Arquitetural:** Desenvolver o sistema utilizando puramente a stack padrão do Django (SQLite, DTL, CBVs) sem APIs REST isoladas ou microsserviços.
* **Identidade Visual Unificada:** Implementar um Design System coeso com TailwindCSS focado em um ambiente de fundo escuro e gradientes harmônicos que se repetem por todo o ecossistema.
* **Autenticação Segura por E-mail:** Substituir o padrão de login por `username` do Django para autenticação direta por `email`, alinhando-se às práticas modernas de UX.
* **Entrega Incremental:** Estruturar o desenvolvimento em Sprints bem delimitadas, adiando testes automatizados e containerização (Docker) para as fases finais de refatoração e polimento.

## 6. Requisitos Funcionais

### RF-001: Landing Page Pública
* O sistema deve exibir uma página inicial institucional pública de apresentação do produto.
* Deve conter links visíveis para as telas de 'Cadastre-se' e 'Login'.

### RF-002: Autenticação de Usuários
* O sistema deve permitir que novos usuários se cadastrem informando e-mail, nome, sobrenome e senha.
* O login deve ser efetuado exclusivamente através da combinação de **E-mail** e **Senha**.
* O sistema deve permitir a desconexão do usuário (Logout) a partir de qualquer tela autenticada.

### RF-003: Dashboard Principal
* Após o login com sucesso, o usuário deve ser redirecionado para o Dashboard Principal.
* O Dashboard deve apresentar o saldo consolidado (soma de todas as contas), total de receitas do mês atual, total de despesas do mês atual e uma listagem das últimas transações realizadas.

### RF-004: Gestão de Contas Bancárias (`accounts`)
* O usuário deve poder cadastrar suas contas (ex: 'Carteira', 'Banco X', 'Investimentos').
* Campos obrigatórios: Nome da Conta, Tipo de Conta (Corrente, Poupança, Dinheiro) e Saldo Inicial.
* Deve ser possível visualizar, editar e excluir uma conta existente.

### RF-005: Gestão de Categorias (`categories`)
* O usuário deve poder criar categorias customizadas para classificar seus fluxos (ex: 'Alimentação', 'Salário', 'Lazer').
* Campos obrigatórios: Nome da Categoria e Tipo (Entrada ou Saída).
* Deve ser possível visualizar, editar e excluir uma categoria existente.

### RF-006: Gestão de Transações (`transactions`)
* O usuário deve poder lançar movimentações financeiras vinculadas a uma Conta e a uma Categoria.
* Campos obrigatórios: Descrição, Valor, Tipo (Entrada/Receita ou Saída/Despesa), Data da Transação, Conta Vinculada e Categoria Vinculada.
* Ao cadastrar ou deletar uma transação, o saldo da conta associada deve ser atualizado de forma correspondente.

### RF-007: Perfil do Usuário (`profiles`)
* O sistema deve manter um registro de perfil atrelado ao usuário para armazenar dados complementares, garantindo isolamento da lógica de autenticação.

---

### Flowchart de UX (Mermaid)

```mermaid
graph TD
    %% Estilo dos Nós
    classDef public fill:#1e1b4b,stroke:#818cf8,stroke-width:2px,color:#fff;
    classDef auth fill:#311042,stroke:#d946ef,stroke-width:2px,color:#fff;
    classDef private fill:#0f172a,stroke:#38bdf8,stroke-width:2px,color:#fff;

    A[Landing Page Pública]:::public -->|Botão Cadastrar| B[Tela de Cadastro]:::public
    A -->|Botão Entrar| C[Tela de Login]:::public
    
    B -->|Formulário Válido| C
    C -->|Autenticação via E-mail| D[Dashboard Principal]:::private
    
    D -->|Menu Lateral / Links| E[Módulo de Contas]:::private
    D -->|Menu Lateral / Links| F[Módulo de Categorias]:::private
    D -->|Menu Lateral / Links| G[Módulo de Transações]:::private
    
    E -->|Ações: Criar/Editar/Excluir| E1[Formulários de Contas]:::private
    F -->|Ações: Criar/Editar/Excluir| F1[Formulários de Categorias]:::private
    G -->|Ações: Criar/Editar/Excluir| G1[Formulários de Transações]:::private
    
    E1 -->|Salvar / Atualizar| D
    F1 -->|Salvar / Atualizar| D
    G1 -->|Salvar / Atualizar| D
    
    D -->|Botão Sair| H[Logout / Redireciona Landing Page]:::auth
    H --> A
```

## 7. Requisitos Não-Funcionais

### RNF-001: Stack e Simplicidade
* O projeto deve ser construído utilizando Python e Django Full Stack (sem APIs separadas, usando o ecossistema interno).
* O banco de dados deve ser unicamente o **SQLite** nativo, sem necessidade de configuração de servidores externos de banco de dados.

### RNF-002: Padrão de Código e Estilo
* Todo o código-fonte deve ser escrito em **Inglês** (nomes de variáveis, classes, models, views, commits, documentação interna).
* O código deve seguir estritamente as diretrizes da **PEP8**.
* Devem ser utilizadas **aspas simples (`'`)** em strings e declarações em todo o projeto, exceto onde a sintaxe exigir aspas duplas.
* Devem ser utilizadas **Class Based Views (CBVs)** nativas do Django (`ListView`, `CreateView`, `UpdateView`, `DeleteView`, `TemplateView`) para manter o padrão enxuto e reutilizável.

### RNF-003: Interface com o Usuário (UI/UX)
* Toda a interface visível ao usuário final deve estar em **Português Brasileiro (pt-BR)**.
* O design deve ser obrigatoriamente **responsivo** (Mobile-first ou adaptável de forma fluida para resoluções menores).
* O fundo de todas as telas autenticadas e públicas deve ser **escuro** (Paleta Dark).
* A interface deve utilizar o utilitário **TailwindCSS** carregado de forma limpa, garantindo a homogeneidade visual.

### RNF-004: Auditoria de Dados
* Toda e qualquer tabela/model criada no banco de dados deve obrigatoriamente herdar ou possuir os campos de auditoria temporal: `created_at` (DateTime de criação, com `auto_now_add=True`) e `updated_at` (DateTime de atualização, com `auto_now=True`).

### RNF-005: Ciclo de Vida do Projeto
* Ambientes de isolamento como Docker e testes automatizados (`tests.py`) estão fora do escopo inicial e só serão implementados nas Sprints finais de consolidação.

## 8. Arquitetura Técnico

### Stack Tecnológica
* **Linguagem:** Python
* **Framework Web:** Django (Full Stack)
* **Engine de Template:** Django Template Language (DTL)
* **Estilização & Design:** TailwindCSS
* **Banco de Dados:** SQLite

### Estrutura de Dados (Database Schema - Mermaid ERD)

```mermaid
erDiagram
    %% Relações entre tabelas
    CustomUser ||--|| Profile : "possui (1:1)"
    CustomUser ||--o{ Account : "possui (1:N)"
    CustomUser ||--o{ Category : "possui (1:N)"
    Account ||--o{ Transaction : "contém (1:N)"
    Category ||--o{ Transaction : "classifica (1:N)"

    CustomUser {
        int id PK
        string email UK "Usado para autenticação"
        string password
        boolean is_active
        boolean is_staff
        datetime created_at
        datetime updated_at
    }

    Profile {
        int id PK
        int user_id FK "Relação OneToOne com CustomUser"
        string first_name
        string last_name
        datetime created_at
        datetime updated_at
    }

    Account {
        int id PK
        int user_id FK "Dono da conta"
        string name "Ex: Banco do Brasil"
        string account_type "Ex: checking, savings, cash"
        decimal balance "Saldo monetário atual"
        datetime created_at
        datetime updated_at
    }

    Category {
        int id PK
        int user_id FK "Dono da categoria"
        string name "Ex: Alimentação"
        string transaction_type "Ex: income, expense"
        datetime created_at
        datetime updated_at
    }

    Transaction {
        int id PK
        int account_id FK "Conta associada"
        int category_id FK "Categoria associada"
        string description "Ex: Compra de supermercado"
        decimal amount "Valor monetário da transação"
        string transaction_type "Ex: income, expense"
        date date "Data da realização"
        datetime created_at
        datetime updated_at
    }
```

## 9. Design System (TailwindCSS & Django Templates)

Para garantir uma identidade visual totalmente coesa, moderna e harmoniosa em modo escuro, fica estabelecido o seguinte conjunto de classes utilitárias do TailwindCSS. Nenhum outro padrão de cor fora deste escopo deve ser misturado aleatoriamente no HTML.

### Paleta de Cores e Fundo
* **Fundo Geral da Aplicação (`Background`):** `bg-slate-900` ou `bg-neutral-950`
* **Fundo de Superfície / Cards / Modais:** `bg-slate-800/60` com bordas `border border-slate-700/50`.
* **Gradiente Primário da Marca (Usado em banners, botões principais e destaques):** `bg-gradient-to-r from-violet-600 via-indigo-600 to-cyan-500`
* **Texto Principal (`Text Primary`):** `text-slate-100` ou `text-white`
* **Texto Secundário (`Text Secondary`):** `text-slate-400`
* **Cores de Status (Financeiro):**
    * *Entradas/Receitas:* `text-emerald-400` / `bg-emerald-500/10`
    * *Saídas/Despesa:* `text-rose-400` / `bg-rose-500/10`

### Padrão de Componentes HTML (Sintaxe DTL com aspas simples)

#### 1. Tipografia e Fontes
A aplicação utilizará a pilha de fontes sans-serif nativa otimizada (`font-sans`), preferencialmente renderizando a fonte Inter do sistema operacional.
```html
<h1 class='text-2xl font-bold tracking-tight text-white sm:text-3xl'>Título da Tela</h1>
<p class='mt-2 text-sm text-slate-400'>Subtítulo explicativo com instruções contextuais.</p>
```

#### 2. Botão Primário (Com Gradiente Harmônico)
```html
<button type='submit' class='inline-flex items-center justify-center px-4 py-2 text-sm font-medium text-white bg-gradient-to-r from-violet-600 to-indigo-600 hover:from-violet-500 hover:to-indigo-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-slate-900 focus:ring-indigo-500 rounded-lg transition-all duration-200 shadow-lg shadow-indigo-600/20'>
    Salvar Registro
</button>
```

#### 3. Botão Secundário / Cancelar
```html
<a href='#' class='inline-flex items-center justify-center px-4 py-2 text-sm font-medium text-slate-300 bg-slate-800 hover:bg-slate-700 border border-slate-700 hover:border-slate-600 rounded-lg transition-colors duration-200'>
    Cancelar
</a>
```

#### 4. Inputs e Formulários
Todos os campos de texto do sistema devem seguir este padrão visual para garantir consistência no preenchimento:
```html
<div class='space-y-1'>
    <label for='id_field' class='block text-sm font-medium text-slate-300'>Nome do Campo</label>
    <input type='text' id='id_field' name='field_name' required
           class='block w-full px-3 py-2 bg-slate-800/80 border border-slate-700 rounded-lg text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 text-sm transition-colors duration-150'
           placeholder='Ex: Digite a informação aqui...'>
</div>
```

#### 5. Layout Estrutural (Grid e Menu Lateral)
Todas as telas autenticadas compartilham a mesma estrutura de casca (*Shell*), com um menu de navegação lateral esquerdo fixo e a área de conteúdo à direita.
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
                </div>
        </main>
    </div>
</div>
```

## 10. User Stories (Histórias de Usuário)

### Épico 1: Autenticação Moderna e Acesso Autenticado
**História de Usuário:** Como um usuário interessado na plataforma, quero me cadastrar e efetuar login usando meu e-mail para acessar com segurança o painel financeiro sem precisar lembrar de um nome de usuário arbitrário.

#### Critérios de Aceite:
* A tentativa de login informando um `username` clássico do Django deve ser impossível; apenas o campo `email` deve ser aceito como identificador único.
* A senha deve ser armazenada com criptografia nativa forte do Django.
* Ao se registrar, o sistema deve criar automaticamente a instância correspondente do usuário e o seu perfil (`profiles`).
* Caso um e-mail já cadastrado tente se registrar novamente, um erro claro em português deve ser exibido.
* Tentativas de acessar o Dashboard ou qualquer rota interna sem estar logado devem redirecionar imediatamente para a tela de Login.

### Épico 2: Gestão de Fluxos e Saldos Financeiros
**História de Usuário:** Como um usuário autenticado, quero cadastrar minhas contas e meus lançamentos de despesas e receitas para ver o impacto direto e em tempo real sobre os meus saldos financeiros consolidados.

#### Critérios de Aceite:
* Ao adicionar uma transação do tipo despesa (`expense`), o valor deve ser subtraído do saldo total da conta bancária vinculada.
* Ao adicionar uma transação do tipo receita (`income`), o valor deve ser somado ao saldo total da conta bancária vinculada.
* Se uma transação for removida, o saldo da conta deve reverter o impacto gerado exatamente pelo montante original daquela transação.
* As visualizações em tabelas devem colorir transações de receita com tonalidades verdes (`text-emerald-400`) e despesas com tons vermelhos (`text-rose-400`).

## 11. Métricas de Sucesso (KPIs)
Para validar a adoção do produto e o bom comportamento técnico da aplicação, os seguintes indicadores serão observados:
1.  **KPI de Retenção de Usuários:** Percentual de usuários que realizam pelo menos 3 lançamentos semanais após o cadastro inicial.
2.  **KPI de Performance de Página:** Tempo médio de carregamento de páginas da área logada (`Dashboard` e `Transactions`) abaixo de 400ms, viabilizado pelo uso de consultas otimizadas no SQLite.
3.  **KPI de Erros de Operação:** Índice de erros HTTP 500 ou quebras de integridade de banco de dados (como orfandade de registros financeiros) mantido em 0%.

## 12. Riscos e Mitigações

* **Risco 1: Concorrência e Conflitos de Escrita no SQLite:** Sendo um banco baseado em arquivo único, cenários de concorrência massiva de acessos simultâneos podem gerar travamentos por *database locked*.
    * *Mitigação:* O Finanpy foi desenhado estritamente como um MVP pessoal e enxuto. O uso de timeouts de conexão configurados no Django settings e índices adequados mitigam completamente a concorrência em baixa/média escala.
* **Risco 2: Complexidade na Atualização de Saldos:** Atualizar o saldo da conta calculando de forma manual e espalhada pelas views pode gerar divergências de saldo quando transações forem editadas ou apagadas.
    * *Mitigação:* Isolar estritamente a recomputação ou centralizá-la usando métodos específicos do Model ou concentrando regras em `signals.py` dedicado dentro de `transactions`, garantindo atomicidade na transação do banco.