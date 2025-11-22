# TaskFlow - Gerenciador de Tarefas

## Descrição

TaskFlow é um sistema de gerenciamento de tarefas desenvolvido em Python que permite aos usuários criar, editar, acompanhar e concluir tarefas com prazos definidos. O sistema foi projetado com foco em segurança, boas práticas de programação e facilidade de uso.

---

## Funcionalidades Principais

### Gerenciamento de Usuários
- Cadastro de Novos Usuários: Criar contas com nome, e-mail, login e senha
- Autenticação Segura: Login com hash SHA256 para proteção de senha
- Controle de Sessão: Gerenciamento de usuário logado
- Logout: Encerramento seguro de sessão

### Gerenciamento de Tarefas (CRUD)
- Criar Tarefas: Adicionar novas tarefas com título, descrição e prazo
- Listar Tarefas: Visualizar todas as tarefas pessoais
- Editar Tarefas: Modificar título, descrição ou prazo existentes
- Concluir Tarefas: Marcar tarefas como concluídas
- Excluir Tarefas: Remover tarefas do sistema
- Relatórios: Gerar relatórios sobre tarefas e prazos

### Estrutura de Dados de Tarefas
Cada tarefa contém:
- id: Identificador único
- título: Nome da tarefa
- descrição: Descrição detalhada
- responsável_id: ID do usuário responsável
- responsável_nome: Nome do responsável
- prazo: Data limite (formato DD/MM/AAAA)
- status: Estado (Pendente, Concluída, Atrasada)
- criação: Data e hora de criação

---

## Estrutura de Arquivos

Task/
- main.py          # Interface principal (menus e fluxo do programa)
- usuarios.py      # Módulo de gerenciamento de usuários
- Tarefas.py       # Módulo de gerenciamento de tarefas
- README.md        # Este arquivo
- utils/
  - arquivos.py    # Funções de leitura/escrita em JSON

---

## Principais Módulos

### main.py
Responsável pela interface do usuário e fluxo principal da aplicação.

Funções:
- menu_principal() - Menu inicial (Login, Cadastro, Sair)
- menu_logado() - Menu após autenticação
- tela_cadastro() - Interface de cadastro de usuários
- tela_login() - Interface de login
- tela_criar_tarefa() - Interface para criar nova tarefa
- tela_editar_tarefa() - Interface para editar tarefa existente

---

### usuarios.py
Módulo de autenticação e gerenciamento de usuários com segurança.

Funções Principais:
- cadastrar_usuario(nome, email, login, senha) - Registra novo usuário
- autenticar_usuario(login, senha) - Realiza login do usuário
- get_usuario_logado() - Retorna usuário em sessão
- logout() - Encerra sessão do usuário
- get_usuario_por_id(user_id) - Busca usuário por ID

Segurança:
- Senhas armazenadas com hash SHA256 (unidirecional)
- Senhas nunca aparecem em texto puro
- Validação de unicidade de login
- Sessão segura sem dados sensíveis

---

### Tarefas.py
Módulo de gerenciamento completo de tarefas (CRUD).

Funções Principais:
- criar_tarefa(titulo, descricao, prazo_str) - Cria nova tarefa
- listar_tarefas() - Exibe todas as tarefas do usuário
- editar_tarefa(tarefa_id, novo_titulo, nova_descricao, novo_prazo) - Modifica tarefa
- concluir_tarefa(tarefa_id) - Marca tarefa como concluída
- excluir_tarefa(tarefa_id) - Remove tarefa do sistema
- gerar_relatorio() - Relatório de tarefas

Status de Tarefas:
- STATUS_PENDENTE: Aguardando execução
- STATUS_CONCLUIDA: Tarefa finalizada
- STATUS_ATRASADA: Prazo vencido sem conclusão

---

## Como Usar

### 1. Executar o Programa
python main.py

### 2. Menu Principal
--- TaskFlow - Gerenciador de Tarefas ---
1. Login
2. Cadastrar Novo Usuário
3. Sair

### 3. Cadastrar Novo Usuário
- Escolha opção 2 no menu inicial
- Forneça: nome completo, e-mail, login e senha
- O sistema validará a unicidade do login

### 4. Fazer Login
- Escolha opção 1 no menu inicial
- Informe login e senha
- O sistema autenticará suas credenciais

### 5. Gerenciar Tarefas
Após login, você terá acesso ao menu de tarefas:
--- Menu de [Seu Nome] ---
1. Minhas Tarefas
2. Criar Nova Tarefa
3. Editar Tarefa
4. Concluir Tarefa
5. Excluir Tarefa
6. Relatórios
7. Logout

#### Criar Tarefa
- Título: Resumo da tarefa
- Descrição: Detalhes sobre o que fazer
- Prazo: Data limite (formato DD/MM/AAAA)

#### Editar Tarefa
- Selecione o ID da tarefa a editar
- Deixe em branco os campos que não quer alterar
- Atualize apenas o necessário

---

## Boas Práticas de Segurança

1. Hash de Senhas: Utiliza SHA256 para criptografia unidirecional
2. Sessão Segura: Nunca armazena senhas em memória
3. Validação de Entrada: Verifica unicidade de login
4. Mensagens Genéricas: "Login ou senha inválidos" (não especifica o erro)
5. Isolamento de Dados: Usuários só veem suas próprias tarefas

---

## Formato de Dados

### Usuários (JSON)
{
  "id": 1,
  "nome": "Gabriela M Silva",
  "email": "gabriela.m.silva@ba.estudante.senai.br",
  "login": "gabriela_silva",
  "senha_hash": "a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3"
}

### Tarefas (JSON)
{
  "id": 1,
  "titulo": "Exemplo de Tarefa",
  "descrição": "Descrição detalhada",
  "responsável_id": 1,
  "responsável_nome": "Gabriela M Silva",
  "prazo": "31/12/2025",
  "status": "Pendente",
  "criação": "2025-11-22 14:30:00"
}

---

## Exemplo de Fluxo Completo

1. Execute: python main.py
2. Escolha: 2 - Cadastrar Novo Usuário
3. Preencha os dados e confirme
4. Retorne ao menu e escolha: 1 - Login
5. Faça login com suas credenciais
6. Escolha: 2 - Criar Nova Tarefa
7. Preencha título, descrição e prazo
8. Veja suas tarefas com: 1 - Minhas Tarefas
9. Edite com: 3 - Editar Tarefa
10. Conclua com: 4 - Concluir Tarefa
11. Faça logout com: 7 - Logout

---

## Requisitos

- Python 3.7+
- Sistema de arquivos (para persistência em JSON)
- Nenhuma dependência externa

---

## Notas Importantes

- Persistência: Dados são salvos em arquivos JSON
- Validação de Datas: Sempre use o formato DD/MM/AAAA
- Login Único: Cada login deve ser único no sistema
- Usuário Responsável: Tarefas são automaticamente atribuídas ao usuário logado

---

## Autor

Desenvolvido como um projeto educacional para demonstrar boas práticas em Python, incluindo:
- Modularização e separação de responsabilidades
- Segurança em autenticação
- Persistência de dados
- Interface interativa com usuário

---

## Licença

Este projeto é de código aberto e disponível para fins educacionais.
